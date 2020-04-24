# tasknet

### Motivation

I don't like most of the pre-existing GTD (Getting Things Done) software productivity tools - they feel really clunky and don't seem maximally helpful. I also would like if other useful behaviors were in the same place, like:

1. A quick guess (given estimated times) as to how overburdened your schedule is
2. A central location to mark down Xeffect cards (see [r/theXeffect](https://www.reddit.com/r/theXeffect/))

### Technical details

This program uses [curses](https://en.wikipedia.org/wiki/Curses_(programming_library)), so it runs in terminal (blazing fast) and completely without external dependencies.

The program is technically laid out using a browser-esque url system, where pages can request a new URL to be loaded as they close. As a result, adding new functionality simply requires writing up a class for that page.

The program may be run by calling "python -m main".