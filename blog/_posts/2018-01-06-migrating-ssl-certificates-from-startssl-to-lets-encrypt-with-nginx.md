---
layout: post
author: "Colin Stevens"
date: 2018-01-06 10:03 AM
author_mail: "&#109;&#097;&#105;&#108;&#064;&#099;&#111;&#108;&#105;&#110;&#106;&#115;&#116;&#101;&#118;&#101;&#110;&#115;.&#099;&#111;&#109;"
title:  "Migrating SSL Certificates from StartSSL to Let's Encrypt with Nginx"
tags: ["sysadmin", "encryption", "nginx"]
---
If you run any webservers and have tried to secure them with [HTTPS](https://en.wikipedia.org/wiki/HTTPS), you are probably well aware of the sorry state of [SSL CAs](https://en.wikipedia.org/wiki/Certificate_authority) and the structure of issuing certificates. In order to get a trusted cert and not shell out hundreds of dollars, most people turned to one of the only viable options, [StartSSL](https://www.startcomca.com/). While this solution worked, it required some knowledge of how certificate chains worked, and some manual certificate generation along with dealing with a pretty terrible web interface.

Luckily the landscape of SSL certificates is beginning to change. [Let's Encrypt](https://letsencrypt.org/) recently started offering a promising easy alternative to building free certificates with companies like StartSSL. Like most things, the documentation is there but lacking in some areas. In an effort to serve those who went through the minor hiccups I did, I can only hope they stumble on this post through a desperate google search and find some answers.

# Differences
Traditionally, a certificate chain needed to be generated for every domain name, usually only include the root tld and a www. subdomains. Let's Encrypt allows you to specify any number of subdomains per web domain root, allowing for a single chain to contain any number of alternate subdomain names. Unfortunately, plans to allow wildcard certificates have not yet been implemented. However this alternate name chaining allows you to use a single cert to serve all of your domains by listing every root tld and all subdomains in the same certificate chain as alternate names. It's here that the Let's Encrypt documentation proves useful. They have developed a nice package to generate these certificates with a package called [Certbot](https://certbot.eff.org/).

# Generating a Certificate Chain
The generation of the certificate chain is fairly straightforward. The `letsencrypt` command offers a nice manual. In general, specifying `certonly` as an argument will generate a certificate chain and place it in `/etc/letsencrypt/live/www/<domain>/`. You can generate a cert for any number of domains and subdomains, so long as each domain with a distinct root defined in nginx is provided with the `-w` flag, with relevant domains after it prefix with the `-d` flag.

For example, if I had a webserver with a root in `/home/web/www/foo` with domain foo.bar and wished to have a certificate for `foo.bar`, `www.foo.bar`, and `baz.foo.bar`, I can specify this with:
{% highlight shell-session %}
$ letsencrypt certonly --webroot -w /home/web/www/foo -d foo.bar,www.foo.bar,baz.foo.bar
{% endhighlight %}

Any number of web root and {,sub}domains can be chained in the command in this manner. For verbosity's sake, if I had an additional domain at example.com with a root specified in nginx as `/var/www` and wanted `xyz.example.com` as a subdomain, I can generate all my domains together in just one command:
{% highlight shell-session %}
$ letsencrypt certonly --webroot -w /home/web/www/foo -d foo.bar,www.foo.bar,baz.foo.bar -w /var/www -d example.com,xyz.example.com
{% endhighlight %}

If all goes well, you should get a message similar to:
{% highlight shell-session %}
Congratulations! Your certificate and chain have been saved at 
  /etc/letsencrypt/live/www.mog.dog/fullchain.pem.
{% endhighlight %}

# Updating Nginx Configuration
Now that we've generated our new certificates, updating your webserver to the newer certificate is a piece of cake. Previous entries that may have looked like this:
{% highlight nginx %}
ssl_certificate /etc/ssl/<domain>/ssl-unified.crt;
ssl_certificate_key /etc/ssl/<domain>/ssl.key;
{% endhighlight %}
Need to be updated to the newly generated files by the certbot. Simply update these two lines to:
{% highlight nginx %}
ssl_certificate /etc/letsencrypt/live/<domain>/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/<domain>/privkey.pem;
{% endhighlight %}

Since all your domains will be listed as alternate names on the single `fullchain.pem` certificate, now might be a good time to move all your SSL-related nginx configurations to a template file that you include with an nginx `include` directive, so SSL settings can be changed across your servers in one file change.

After this, test your configuration with:
{% highlight shell-session %}
$ nginx -t
{% endhighlight %}
And restart the nginx service and you should begin to serve the new certificates.

# Possible Issues: Unauthorized/Failed Authorization Procedure
You may encounter an error generating a certificate on one of your domain roots due to unauthorized access. In this case you should get a `Type: unauthorized` error under the affected domain. This is usually caused by the domain being affected by an nginx `auth_basic` protection. You do not need to disable protection for this domain, but only for a `/.well-known/acme-challenge` folder in the server configuration so that the certbot can verify the domain with its challenge files.

This kind of issue will yield an error similar to the following in nginx's `err.log`:
{% highlight nginx %}
xxx.xxx.xxx.xxx - - [01/Oct/2016:00:16:50 -0400] "GET /.well-known/acme-challenge/jwSHol-m6tYeeErZgS0XpIl9nq5d62ZSYOil2jtIC-E HTTP/1.1" 401 188 "http://<affected domain>/.well-known/acme-challenge/jwSHol-m6tYeeErZgS0XpIl9nq5d62ZSYOil2jtIC-E" "Mozilla/5.0 (compatible; Let's Encrypt validation server; +https://www.letsencrypt.org)"
{% endhighlight %}

To fix this, place a location block similar to the one that follows in the server location using nginx's `auth_basic` functionality:
{% highlight nginx %}
location '/.well-known/acme-challenge' {
    auth_basic off;
    default_type "text/plain";
    root <matching document root specified for server block>;
}
{% endhighlight %}

# Additional Resources
* <https://community.letsencrypt.org/t/failed-authorization-procedure-the-client-lacks-sufficient-authorization-incorrect-validation-certificate-for-tls-sni-01-challenge/16206>
* <https://serverfault.com/questions/330580/enable-basic-auth-sitewide-and-disabling-it-for-subpages>
* <https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04>
* <https://certbot.eff.org/#ubuntuxenial-nginx>
* <https://certbot.eff.org/>
