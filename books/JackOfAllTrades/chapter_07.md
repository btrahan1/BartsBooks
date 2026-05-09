# Chapter 7: Miller Dynamics

The lobby of Miller Dynamics smelled of floor wax and quiet desperation.
A receptionist, who looked like she'd been crying in the breakroom,
buzzed Jack through after he dropped Ted's name and mentioned he had an
appointment with Mr. Henderson.

Mr. Henderson's office was large, wood-paneled, and littered with empty
coffee cups and balled-up paper. Henderson himself looked like a bulldog
who'd lost his chew toy---jowls sagging, eyes bloodshot, tie loosened to
a point of surrender.

He looked at Jack with deep skepticism. Jack wasn't wearing a suit. He
was wearing khakis and a polo shirt that was neat but decidedly
un-corporate. In his hand, he held a chunky, modified barcode scanner
he'd scavenged from an old retail liquidation and duct-taped to a
portable battery pack.

"Run that by me again, Jack?" Henderson asked, rubbing his temples.

Jack placed the scanner on the mahogany desk. It looked comically out of
place next to the gleaming brass nameplate.

"The inventory system," Jack said, his voice calm and level. "Ted tells
me your guys are spending thirty seconds logging a single screw. That's
inefficient. It breaks the flow state. When a mechanic is in the zone,
thirty seconds is an eternity. So, they don't do it. Then your data is
garbage. Then you order parts you don't need."

Jack pulled out his phone. He opened the app he'd hacked together the
night before. It wasn't pretty. The user interface was just gray buttons
and black text. No animations. No logos. Pure function. He'd written it
in Python, using an open-source library for database management he'd
found at 2 AM.

"This," Jack said, tapping the phone, "is a middleware patch. I call it
' The Button'."

He picked up the scanner. "I went down to the floor before I came up
here. I printed these." He tossed a sheet of stickers onto the desk.
They were QR codes. "You stick one on every bin. Screw. Bolt. Washer.
Valve."

"Okay..." Henderson leaned forward.

"Watch." Jack pointed the scanner at a sticker he'd slapped on his own
coffee cup for demonstration. *Beep.*

Instantly, Jack's phone screen flashed green. **COUNT +1**.

"That's it?" Henderson asked.

"That's it," Jack said. "No login. No twelve-digit code. No navigating
three menus to find the 'Restock' sub-folder. The mechanic walks by,
grabs a handful of screws, points the wand, *beep*, and keeps walking.
The app logs the timestamp and the item ID. At the end of the shift, the
app dumps a CSV file directly into your fancy ERP system's backend."

Henderson frowned. "But... security? Who logged it? What job number is
it for?"

"Doesn't matter," Jack said, cutting him off gently. "You don't need to
know *who* took the screw. You need to know that the screw is *gone* so
you can order another one. You're trading perfect data for *actionable*
data. Right now, you have 0% accuracy because the system is too hard to
use. With this, you'll get maybe 95% accuracy. Maybe a guy forgets to
scan once in a while. But 95% is enough to keep the line moving. 95%
means you don't shut down for lack of aluminum."

"Are you saying the mechanics can just point that wand thingee at the
barcode on the different containers of parts, and they won't have to
enter it by hand?"

"Exactly. One second per transaction. Frictionless."

Henderson stared at the taped-up scanner. He looked at the ugly app on
the phone. Then he looked at the pile of overdue production reports on
his desk.

"IT told me rewriting the interface would take six months and cost fifty
grand," Henderson muttered.

"IT wants to rebuild the engine," Jack shrugged. "I just changed the oil
filter. It took me four hours and cost me zero dollars, plus the price
of a scanner I found in a dumpster behind a Radio Shack three years
ago."

Henderson picked up the scanner. He pointed it at the sticker. *Beep.*
The phone counted up. A small, confused smile broke through the man's
exhaustion.

"It... it just works."

"It works," Jack agreed. "It's not pretty. It's not perfect. But it
works."

Henderson looked up, a spark of something like hope in his eyes. "You
said 'let's solve one problem at a time.' This is one. What's the next
one?"

Jack leaned back in the chair, crossing his legs. "Well, Ted tells me
your engineers are fighting a war against physics with your lathes. I'm
not an engineer, but I do know a little bit about vibration dampening. I
think I read somewhere that you can use simple rubber isolators to cheat
the tolerance specs. Want to take a walk down to the floor?"

