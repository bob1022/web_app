Possible addition - One thing you might consider later is displaying both:

Distance: 778.01 KPC
(2.54 million LY)

but that's a future enhancement, not a bug fix.


# A Documentation Note

This is actually a perfect example of something to document:

# Travel Time Calculator

Destination Dropdown

Source:
space_objects

Flow:
Python variable
    ↓
render_template()
    ↓
travel_time.html
    ↓
Jinja for loop
    ↓
Dropdown options

That's exactly the kind of "how does this work?" note that helps bridge the gap between using code and understanding code.