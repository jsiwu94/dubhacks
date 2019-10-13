# Prop

![alt text](https://github.com/jsiwu94/dubhacks/blob/master/72161681_455228788672444_4484030811477114880_n.png)


# Inspiration
Fast pace of the modern era has induced a great deal of stress among people, especially amongst Millennials and Generation Z population. While there are apps which provide aid in maintaining with mental and physical health (such as fitness and nutrition app), there are no applications dedicated explicitly to measure and promote happiness and stress level on a regular basis.

# What it does
It allows clients to detect their happiness level on a daily basis based on various channels. Prop measures clients' text interaction on Twitter, Facebook, Instagram, Whatsapp, Gmail, Search History along with music (Spotify) and movie (Netflix) preferences, to come up with a score index that monitors happiness ranging from -1 to 1.

We also provide a chart which the historical index, and thus motivates the clients to strive for better happiness levels.

The index range breakdown is as below :
-1 to -.8 --> very negative
-.8 to -.5 --> negative
-.5 to -.3 --> somewhat negative
-.3 to .3 --> neutral
.3 to .5 --> somewhat positive
.5 to .8 --> positive
.8 to 1 --> very positive

def score_range(score):
        if score <= -.8:
            o = -.8
        elif score > -.8 and score <= -.5:
            o = -.5
        elif score > -.5 and score <= -.3:
            o = -.3
        elif score > -.3 and score <= .3:
            o = 0
        elif score > .3 and score <= .5:
            o = .3
        elif score > .5 and score <= .8:
            o = .5
        else:
            o = .8
        return(o)


# How we built it


# Accomplishments that we're proud of


# What we learned


# What's next for Prop
