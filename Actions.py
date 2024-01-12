import yaml
import os
from os import path

def action_Data():
    customActions_path = "dependencies/customActions.yml"

    if path.exists(customActions_path) == False:
        with open(customActions_path, "w") as action:  # Create config file if one does not exist
            action.write("# Custom client actions info...\n"
                         "# Click coords should remain inside 900 x 700 pixels. Some useful coords are:\n"
                         "# 47, 663 for habbo logo in bottom left\n"
                         "# 287, 611 for the chat box\n"
                         "# Delay adjusts the time in seconds before the action is executed after entering the room.\n"
                         "# Example actions are found bellow. Real actions should not contain '#' infront. Action names can be set as anything.\n"
                         "# Actions are executed in the order they are listed bellow from top to bottom, Unless the set delay overlaps another actions delay time.\n\n"
                         "#customAction1:\n"
                         "#  type: click\n"
                         "#  click_button: left\n"
                         "#  coords: 103, 667\n"
                         "#  delay: 1\n\n"
                         "#customAction2:\n"
                         "#  type: chat\n"
                         "#  message: custom message goes here\n"
                         "#  delay: 1\n\n"
                         "EnterHomeRoom:\n"
                         "  type: click\n"
                         "  click_button: left\n"
                         "  coords: 45, 660\n"
                         "  delay: 2\n\n")
            # yaml.dump(example_dict, action, default_flow_style=False)

    def yaml_read(path):
        with open(path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)

    # Load the config file into a dictionary
    actions = yaml_read(customActions_path)

    parsed_actions = {}

    for key, value in actions.items():
        parsed_actions[key] = value

    return parsed_actions

# If Actions.py is run directly, then print all actions from customActions.yml to console.
if __name__ == "__main__":

    # Test function to test parsing data from yaml file to python function variables
    def test_func(type, message="Automated chat message!", coords=(0, 0), click_button="left", delay=1):
        print(type)
        if type == "click":
            print(coords)
            print(click_button)
            print(delay)
        elif type == "chat":
            print(message)
            print(delay)

    # Save output of action_Data function as a dictionary
    custom_actions_data = action_Data()

    # Save each of the dictionary values as their respective variable types and parse them to test_func
    for action_name, action_details in custom_actions_data.items():
        action_type = action_details.get('type', '')
        action_message = action_details.get('message', 'Automated chat message!')
        action_coords = tuple(map(int, action_details.get('coords', '0, 0').split(',')))
        action_click_button = action_details.get('click_button', 'left')
        action_delay = int(action_details.get('delay', 1))

        print("\n----------\n")

        test_func(type=action_type,
                  message=action_message,
                  coords=action_coords,
                  click_button=action_click_button,
                  delay=action_delay
                  )