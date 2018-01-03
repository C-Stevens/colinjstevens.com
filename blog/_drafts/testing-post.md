---
layout: post
author: "Colin Stevens"
author_mail: "mail@colinjstevens.com"
title:  "Testing post"
categories: misc
tags: ["foo", "bar",  "baz" ]
---

# Hello and welcome to this test post
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras consectetur dolor sit amet est luctus cursus. Fusce ac ullamcorper ipsum. Sed massa massa, consectetur quis cursus malesuada, mattis semper dui. Aenean condimentum, massa in ullamcorper iaculis, dolor purus pellentesque ipsum, eu iaculis eros dui eu nibh. Proin eleifend dictum mi, eget vehicula ipsum posuere vel. Curabitur a tincidunt magna, a aliquam ipsum. Ut ac ipsum vitae erat eleifend fermentum. Aliquam semper enim ut turpis sagittis bibendum. Donec vel pulvinar lectus.

## This is a subheading
Cras dui turpis, tincidunt id mi in, mattis elementum erat. Curabitur tristique id massa suscipit vehicula. Quisque sem justo, dignissim nec leo ut, pharetra aliquam quam.

Here's some code:
{% highlight ruby %}
def show
  @widget = Widget(params[:id])
  respond_to do |format|
    format.html # show.html.erb
    format.json { render json: @widget }
  end
end
{% endhighlight %}

And with line numbers:
{% highlight ruby linenos %}
def show
  @widget = Widget(params[:id])
  respond_to do |format|
    format.html # show.html.erb
    format.json { render json: @widget }
  end
end
{% endhighlight %}
