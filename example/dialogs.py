# This Python file uses the following encoding: utf-8

bot = {'en':{
               'command_failed': "Sorry, something went wrong. "
               "Need help? Type: '/%s help'.",
               },
       'nl':{
               'command_failed': "Sorry, er ging iets mis. "
               "Hulp nodig? Type: '/%s help'"
               }
      }

bbq = {'en':{
               'usage': "The command /bbq determines if the weather "
               "circumstances in the Netherlands are suitable for barbecuing.",
               'reply': "On a scale of 1-10, the barbecue weather in the "
               "Netherlands gets an %s."
               },
       'nl':{
               'usage': "Het commando /bbq geeft het huidige "
               "barbecueweercijfer voor Nederland.",
               'reply': "Het barbecueweer krijgt vandaag een %s. Oant moarn!"
               }
      }

dice = {'en':{
               'usage': "Throw a die with /dice. Throw multiple dice by "
               "adding a number. For example: /dice 2.",
               'reply': "You threw: %s.",
               'reply_0': "Please throw at least 1 die.",
               'reply_max': "Sorry, the maximum number of dice you can throw "
               "is 10."
               },
       'nl':{
               'usage': "Gooi een dobbelsteen met /dice. Om meerdere "
               "dobbelstenen voeg je een getal toe. Bijvoorbeeld: "
               "'/dice 2'.",
               'reply': "Je gooide %s.",
               'reply_0': "Gooi ten minste 1 dobbelsteen, alsjeblieft.",
               'reply_max': "Sorry, het maximum aantal dobbelstenen dat je kan "
               "gooien is 10."
               }
      }

doge = {'en':{
               'usage': "Create your own doge image with '/doge "
               "[your caption]'. For example: '/doge wow such example'."
               },
       'nl':{
               'usage': "Maak je eigen doge plaatje met '/doge [caption]'."
               "Bijvoorbeeld: '/doge wow such example'."
               }
      }

echo = {'en':{
               'usage': "The simplest command there is: '/echo [text]' returns "
               "your [text]."
               },
         'nl':{
               'usage': "Het meest simpele commando dat er is: '/echo [tekst]' "
               "retourneert jouw [tekst]."
               }
      }

google = {'en':{
               'usage': "Search the internet with Google using '/google "
               "[query]'.",
               'reply_top': "Top %d hits for '%s':\n",
               'reply_bottom': "For more results: %s",
               'no_results': "Sorry, no results found for '%s'."
               },
         'nl':{
               'usage': "Doorzoek het internet met Google: '/google "
               "[zoekterm]'.",
               'reply_top': "Top %d hits voor ''%s':\n",
               'reply_bottom': "Voor meer resultaten: %s",
               'no_results': "Sorry, geen resultaten gevonden voor '%s'."
               }
      }

help = {'en':{
               'usage': "Help-ception! Please try /help for a list of "
               "commands.",
               'reply': "Here is a list of all available commands:"
               },
       'nl':{
               'usage': "Help-ception! Probeer /help voor een lijst met alle "
               "beschikbare commando's.",
               'reply': "Hier is een lijst met alle beschikbare commando's:"
               }
      }

gif = {'en':{
               'usage': "Search for gifs using '/gif [search query]'. You can ask"
               " for a random gif using '/gif random [optional search query]'.",
               'no_results': "Sorry, no gifs found for query '%s'."
               },
         'nl':{
               'usage': "Zoek naar gifs met '/gif [zoekterm]'. Je kunt ook een "
               "willekeurige gif opvragen met '/gif random [optionele zoekterm]'",
               'no_results': "Sorry, geen gifs gevonden voor '%s'."
               }
      }

poll = {'en':{
               'usage': "Start a poll! Use the following format: '/poll "
               "[question] *[option 1] *[option 2] *[etc]'. You can always "
               "/cancel a poll and ask for the /results.",
               'store_answer': "Thanks, your answer has been recorded.",
               'results': "The results for '%s':",
               'end_poll': "The poll has ended.",
               'not_owner': "Sorry, you are not the owner of the current poll. "
               "Only the owner can /cancel it.",
               'poll_already_active': "Sorry, another poll is already active. "
               "The owner must /cancel the current one first.",
               'votes': "votes", 'vote': "vote"
               },
         'nl':{
               'usage': "Start een poll! Gebruik het volgende formaat: "
               "'/poll [vraag] *[optie 1] *[optie 2] *[etc]'. De resultaten "
               "kunnen opgevraagd worden met /results en de poll kan "
               "geannuleerd worden met /cancel.",
               'store_answer': "Dankjewel, je antwoord is opgeslagen.",
               'results': "De resultaten voor de vraag '%s':",
               'end_poll': "De poll is beëindigd.",
               'not_owner': "Sorry, je bent niet de eigenaar van de actieve "
               "poll. Alleen de eigenaar can de poll annuleren met /cancel.",
               'poll_already_active': "Sorry, er is al een andere poll actief. "
               "De eigenaar moet de huidige poll eerst annuleren met /cancel.",
               'votes': "stemmen", 'vote': "stem"
               }
      }

putin = {'en':{
               'usage': "The command /putin returns a random photo of "
               "Vladimir Putin."
               },
         'nl':{
               'usage': "Het /putin commando retourneert een willekeurige "
               "foto van Vladimir Putin."
               }
      }

quote = {'en':{
               'usage': "Save quotes by using '/quote [name]: [quote]'. "
               "You can also ask for a random quote using '/quote [optional "
               "name]'. Request all quotes by adding 'all'.",
               'quote_saved': "Quote saved."
               },
         'nl':{
               'usage': "Sla je quotes op met behulp van '/quote [naam]: "
               "[quote]'. Een willekeurige quote is aan te vragen met '/quote "
               "[optionele naam]'. Vraag alle quotes op door 'all' toe te "
               "voegen.",
               'quote_saved': "Quote opgeslagen."
               }
      }

stats = {'en':{
               'usage': "The /stats command returns statistics of the "
               "chat.",
               'reply': "Total messages sent: %i\n"
               "Total words sent: %i\n\n"
               "Top 3 most used commands:\n"
               "1. %s (%i times)\n2. %s (%i times)\n3. %s (%i times)\n\n"
               "Top 3 most active users (number of messages):\n%s",
               'error': "Sorry, not enough data yet. Chat some more!"
               },
         'nl':{
               'usage': "Het /stats commando geeft de huidige "
               "gespreksstatistieken.",
               'reply': "Totaal verzonden berichten: %i\n"
               "Totaal verzonden woorden: %i\n\n"
               "Top 3 meest gebruikte commando's:\n"
               "1. %s (%i keer)\n2. %s (%i keer)\n3. %s (%i keer)\n\n"
               "Top 3 meest actieve gebruikers (aantal berichten):\n%s",
               'error': "Sorry, nog niet genoeg data. Chat nog wat meer!"
               }
      }

status = {'en':{
               'usage': "The /status commands lets you know the current status "
               "of the bot.",
               'reply': "PyBot is up and running. Awaiting your commands."
               },
         'nl':{
               'usage': "Het /status commando geeft de huidige status weer van "
               "de bot.",
               'reply': "PyBot staat voor je klaar en wacht op je commando."
               }
      }

weather = {'en':{
               'usage': "Get the actual weather with '/weather [place name]'.",
               'lang': 'en',
               'error': "Sorry, no results found for '%s'.",
               'reply': "It's %s degrees Celsius in %s. Weather description: "
               "%s."
               },
         'nl':{
               'usage': "Krijg de actuele weersomstandigheden met '/weather "
               "[plaatsnaam]'.",
               'lang': 'nl',
               'error': "Sorry, geen resultaten gevonden voor '%s'.",
               'reply': "Het is %s graden in %s. Weersomstandigheden: %s."
               }
      }

wiki = {'en':{
               'usage': "Search wikipedia using '/wiki [query]'. For example: "
               "'/wiki Albert Einstein'.",
               'no_results': "Sorry, no results found for '%s'."
               },
         'nl':{
               'usage': "Doorzoek wikipedia met '/wiki [zoekterm]'. "
               "Bijvoorbeeld: '/wiki Albert Einstein'.",
               'no_results': "Sorry, geen resultaten gevonden voor '%s'."
               }
      }

youtube = {'en':{
               'usage': "Search YouTube with '/youtube [query]'. The first "
               "result is then returned.",
               'no_results': "Sorry, no results found for '%s'."
               },
         'nl':{
               'usage': "Doorzoek YouTube met '/youtube [zoekterm]'. Het "
               "eerste resultaat wordt gegeven.",
               'no_results': "Sorry, geen resultaten gevonden voor '%s'."
               }
      }

empty = {'en':{
               'usage': ""
               },
         'nl':{
               'usage': ""
               }
      }
