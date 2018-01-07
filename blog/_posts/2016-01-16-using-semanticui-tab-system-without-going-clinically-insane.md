---
layout: post
author: "Colin Stevens"
date: 2016-01-16 2:03 AM
author_mail: "&#109;&#097;&#105;&#108;&#064;&#099;&#111;&#108;&#105;&#110;&#106;&#115;&#116;&#101;&#118;&#101;&#110;&#115;.&#099;&#111;&#109;"
title:  "Using Semantic-UI's Tab System without going Clinically Insane"
tags: ["webdev", "html", "javascript", "semantic-ui", "nginx"]
---
[Semantic-UI](https://semantic-ui.com/) is a really neat and pretty alternative to other UI libraries (like [bootstrap](http://getbootstrap.com/)), not to mention the fact that it's heavily community driven. However, its documentation – despite being mostly thorough – is *just* vague enough in all the right places to cause some major headaches. For example, their fairly new [tabbing system](https://semantic-ui.com/modules/tab.html).

With help from a friend and a horrific amount of hair-pulling, I was able to get something working and hope to fill in some of the documentation gaps with some straightforward tips. So, let's get started.

# Start from Scratch
Hopefully by the time you read this you haven't already started your project too far, or (god forbid) aren't trying to update an existing Semantic site to add a functional tab system.

By far the best way to get substantive results is to start from scratch and build up slowly, getting the tabs functional before you invest too much time anywhere else. I recommend using the [template example](https://gist.github.com/C-Stevens/757e0e1bb3f7bbc04fe1) I made while rebuilding my personal site as a skeleton to gut and rework into your own uses.

## What You'll Need
The template I've made might not weather the years very well as Semantic gets updates, and it uses relative imports of some files. If you're using and gutting this example, or running a new site from scratch, there are some imports you'll need to consider (listed here for your convenience):

* [Semantic's CSS rules](http://oss.maxcdn.com/semantic-ui/2.1.8/semantic.min.css) - Not strictly speaking required as it's just to make things look pretty, but it's listed here because you'll more than likely want it.
    * If you want to run an even more lightweight site, you can include only [Semantic's tab CSS](http://oss.maxcdn.com/semantic-ui/2.1.8/components/tab.min.css) styling rules.
* [Semantic's Javascript](http://oss.maxcdn.com/semantic-ui/2.1.8/semantic.min.js)
    * Like the above, you can import only the relevant [tab script](http://oss.maxcdn.com/semantic-ui/2.1.8/components/tab.min.js) to make a lighter site.
* [jQuery](https://code.jquery.com/jquery-2.2.0.min.js) - Version 2.2.0 at the time of this writing.
* [Asual's jQuery Address library](https://github.com/asual/jquery-address) – Other than jQuery, this is the only other non-Semantic third party library you'll need to import.

## Import Ordering

I've run into some headaches before and have found (at least) one importing order that achieves results. I'm sure there are other ways to order the imports while maintaining functionality, but I'll stick to what I know works. The order is:
1. Semantic.css – imported in the HTML head.
2. jQuery – imported under the tab HTML.
3. Address.js – ditto, but placed underneath the above.
4. Semantic.js – ditto.
5. Custom Javascript – at the very end is where I've found the safest place to put the javascript used to initialize and setup the Semantic tabbing system.

# Start with the Basic HTML
Start out with only what you'll need to get basic tabs up and running. For my example this amounted to just:
{% highlight html %}
<div id="menu_bar">
    <div class="ui pointing links secondary menu">
        <div class="ui text container">
            <a class="item" data-tab="about">About</a>
            <a href="#" class="item">Blog</a>
            <a class="item" data-tab="cv">CV</a>
            <a class="item" data-tab="contact">Contact</a>
        </div>
    </div>
    <div class="ui tab segment" data-tab="about">
        About
    </div>
    <div class="ui tab segment" data-tab="cv">
        CV
    </div>
    <div class="ui tab segment" data-tab="contact">
        Contact
    </div>
</div>
{% endhighlight %}
I then placed CSS styling at the end of the page for safety and inline, but it more than likely can be safely imported in the HTML head.

Keep in mind that your tabs and tab data divs need to be nested inside the menu container (In this example, "#menu_bar").

# Get the Javascript Right
This is another place where the Semantic docs do a great job at explaining all sorts of things, but none of the examples give quite enough help. This is the JavaScript that you'll need to use, after all your other scripts have been imported, to enable tabbing:
{% highlight javascript %}
$('#menu_bar .menu .item').tab({
     history : true,
     context : '#menu_bar',
     historyType : 'state',
     path        : '/',
});
{% endhighlight %}
Take note of the jQuery selector used (In this example, "#menu_bar .menu .item") here. This **must** point to the id of the div containing your menu, and include the menu and item classes. Additionally, **if you change the menu div id**, you must update the "context" field in this script to match it as well.

This also assumes here that you want your tabs to exist on the root of your webpage (i.e you would have yourdomain.tld/tab1 and yourdomain.tld/tab2, etc.). If you want this root to be different (e.g yourdomain.tld/content/tab1), you need to change the context value in the script.

# Configure the Backend
This set of notes will assume you're using [nginx](http://nginx.org/) as your webserver. If you use something else, like [Apache](http://www.apache.org/), you'll need to modify this basic configuration appropriately. The Semantic docs do a horrific job at explaining this step, but luckily it's pretty easy. A basic nginx configuration needed to have a functional site with tabbing capabilities can be done like this:
{% highlight nginx %}
server {
    listen                      80;
    server_name                 your.site.tld;
    root                        /var/run/foo/bar;
    index                       index.html;
    location / {
        rewrite               /(about|cv|contact)/? /index.html;
    }
}
{% endhighlight %}
And of course update the tab names in the regex to reflect the data-tab names you used on your site.

**Note:** If you used a document root other than "/" while setting up your JavaScript to enable tabbing, you will need to update your rewrite line to use the root path other than just expecting requests to "/" as in the above example.

# That's it
The above tips should get you up and running but if you're still having trouble, stripping the site down lighter or restarting from scratch eliminates a lot of variables that may be interfering.
