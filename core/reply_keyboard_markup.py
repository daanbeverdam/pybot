class ReplyKeyboardMarkup():
    """Contains a custom keyboard which will be sent by the bot."""
    def __init__(self):
    	self.keyboard = None  # array of array of strings like [['a'],['b']]
    	self.hide_keyboard = False  # will hide the keyboard if True
        self.resize_keyboard = True
        self.one_time_keyboard = True
        self.selective = False
