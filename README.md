# beeshop
My attempt at a chess AI written in Python, compatible with Lichess

I take no responsibility for the pun in the name

### Things to install

*If just using engine.py*

`pip install chess`

`pip install pyinstaller`

Replace `from dbai import find_move` with your own engine

Then run `pyinstaller engine.py -F` and follow [lichess bot instructions](https://github.com/ShailChoksi/lichess-bot)

*If using dbai.py*

`pip install requests`

\+ Everything from engine.py

*If using vision system*

Don't. It's there if you want it but I'm not making a guide on how to set it up anytime soon as it's a little too indepth.