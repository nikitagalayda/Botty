jokes = [
	"I would tell you a UDP joke, but you might not get it.",
	"How many computer programmers does it take to change a light bulb? None, that's a hardware problem",
	"A programmer is at work when his wife calls and asks him to go to the store. She says she needs a gallon of milk, and if they have fresh eggs, buy a dozen. He comes home with 12 gallons of milk.",
	"Knock knock. Race condition. Who's there?",
	"A guy walks into a bar and asks for 1.4 root beers. The bartender says: I'll have to charge you extra, that's a root beer float. The guy says: In that case, better make it a double.",
	"A programmer puts two glasses on his bedside table before going to sleep. A full one, in case he gets thirsty, and an empty one, in case he doesn’t.",
	"Java and C were telling jokes. It was C's turn, so he writes something on the wall, points to it and says 'Do you get the reference?' But Java didn't.",
	"In order to understand recursion you must first understand recursion.",
	"Knock knock. Who's there? Broken state machine. Broken state machine, who? Knock knock.",
	"Why do programmers confuse halloween and christmas? Because Oct 31 = Dec 25.",
	"Why did the two functions stop calling each other? Because they had constant arguments.",
	"A programmer quit his job because he didn't get arrays",
	"'Honey, go to the store and buy some eggs.' 'OK.' 'Oh and while you're there, get some milk.' He never returned.",
	"Developers use dark IDE themes because bugs are attracted to the light.",
	"How long does a loop last? For a while.",
]

fun_facts = [
	"In Switzerland, it is illegal to own just one guinea pig.",
	"If you lift a kangaroos tail off the ground, it can't hop.",
	"Bananas are curved because they grow towards the sun.",
	"Approximately 10-20%% of U.S. power outages are caused by squirrels.",
	"There are approximately 100,000 hairs on an average human head.",
	"There are more English speakers in China than in the United States.",
	"It takes an average person 7 minutes to fall asleep.",
	"Scotland’s national animal is a unicorn.",
	"People spend an average 22 years of their life asleep.",
	"The average person spends only 10 minutes a day speaking.",
	"Sharks do not get cancer.",
	"An average raindrop falls at the speed of roughly 7 miles an hour.",
	"The eye of an ostrich is bigger than the brain.",
	"Elephants are the only mammals that cannot jump.",
	"More people get attacked every year by a cow than by a shark.",
]

class FunGenerator:
	def __init__(self, joke_counter, fact_counter):
		self.joke_counter = joke_counter
		self.fact_counter = fact_counter

	def tell_joke(self):
		if self.joke_counter != len(jokes):
			curr_joke = jokes[self.joke_counter]
			self.joke_counter+=1
			return curr_joke
		else:
			joke_counter = 0
			return jokes[joke_counter]


	def tell_fact(self):
		if self.fact_counter != len(fun_facts):
			curr_fact = fun_facts[self.fact_counter]
			self.fact_counter+=1
			return curr_fact
		else:
			self.fact_counter = 0
			return fun_facts[fact_counter]
