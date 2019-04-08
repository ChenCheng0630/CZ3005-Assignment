from pyswip.prolog import Prolog
import easygui
import random

# setting up the connection between prolog and python
title = "Kid's day at school."
KB_file = "knowledge_base.pl"
prolog = Prolog()
prolog.consult(KB_file)

activity_positive_suffix = ["as well?", "also?", "too?"]
activity_negative_prefix = ["ok then.", "Nevermind then.", "Alright, how about......hmm..."]
activity_negative_suffix = ["instead?", "?"]

positive_comfort = ["That is so great!", "It is nice to hear that!", "I hope you enjoy next time as well!"]
negative_comfort = ["It's ok..", "It won't be like this everytime.."]

action_negative_prefix = ["Maybe try next time.", "There is no harm doing that right?", "You are encouraged to do that you know?"]

# ask for a particular activity item.
def ask(query, prefix, suffix):
    message = "{} Was there {} today {}".format(prefix, query, suffix)
    return easygui.ynbox(message, title, ("Yes", "No"))

# ask the kid for description of the activity.
def ask_description(query, prefix, suffix):
	message = "{} Was it {} {}".format(prefix, query, suffix)
	return easygui.ynbox(message, title, ("Yes", "No"))

# ask the kid for actions wether he has done.
def ask_action(query, prefix, suffix):
	message = "{} Did you {} {}".format(prefix, query, suffix)
	return easygui.ynbox(message, title, ("Yes", "No"))

# retrive one positive or negative decription of a particular catogry of activity in the KB
def retrive_related_decription(query, positive = True):
	if positive:
		call = "followup_positive_description({}, X)".format(query)
		result = list(prolog.query(call))
		result = random.choice(result)["X"]
		print(result)
		return result
	else:
		call = "followup_negative_description({}, X)".format(query)
		result = list(prolog.query(call))
		result = random.choice(result)["X"]
		print(result)
		return result

# retrive all the actions the kid is supposed to do under a catogry
def retrive_related_actions(query):
	call = "followup_action({}, X)".format(query)
	result = list(prolog.query(call))
	result = [" ".join(i["X"].split('_')) for i in result]
	return result

# sending cooresponding reply according to kid's description
def send_comfort(positive):
	if positive:
		easygui.msgbox(random.choice(positive_comfort))
	else:
		easygui.msgbox(random.choice(negative_comfort))

# ask about whether the kid has done an activity
def ask_about_activity(positive_feedback, activity_item):
	if positive_feedback:
		prefix = ""
		suffix = random.choice(activity_positive_suffix)
	else:
		prefix = random.choice(activity_negative_prefix)
		suffix = random.choice(activity_negative_suffix)
	return ask(activity_item, prefix, suffix)

# ask about the kid's feeling towards one activity he has done.
def ask_about_description(activity_item):
	description_item = retrive_related_decription(activity_item)
	positive_feedback = ask_description(description_item, "Can you describe it?", "?")
	if positive_feedback:
		send_comfort(positive = True)
	else:
		description_item = retrive_related_decription(activity_item, positive = False)
		negative_feedback = ask_description(description_item, "hmm? then...", "?")
		if negative_feedback:
			send_comfort(positive = False)
		else:
			easygui.msgbox("Don't worry, it will get better")

# ask about whether the kid has done the actions he is supposed to do.
def ask_about_action(activity_item):
	actions = retrive_related_actions(activity_item)
	if len(actions) == 0:
		return
	positive_feedback = ask_action(actions[0], "Oh, by the way,", "?")
	for items in actions[1:]:
		if positive_feedback:
			prefix = "That's nice!"
			suffix = "as well?"
		else:
			prefix = random.choice(action_negative_prefix)
			suffix = "then?"
		positive_feedback = ask_action(items, prefix, suffix)


def main():
		activity_item = "slides"
		positive_feedback = True
		has_done = ask(activity_item, "Welcome back kiddo, how is school today?", "?")
		while True:
			if has_done:
				# ask if the kid has positive feeling towards the activity.
				ask_about_description(activity_item)
				# ask if the kid has done correct actions after the activity
				ask_about_action(activity_item)
			else:
				# marking that negative feedback was received.
				positive_feedback = False

			prolog.assertz("history({})".format(activity_item))
			next_items = list(prolog.query('ask(X, {})'.format(activity_item)))
			if len(next_items) == 0:
				break
			activity_item = next_items[0]['X']
			# react differently according to previous feedback
			has_done = ask_about_activity(positive_feedback, activity_item)

		# sending closing message to the user
		easygui.msgbox("That's all, gald we had this conversation!")

if __name__ == "__main__":
	main()
