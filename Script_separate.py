import re


def separate_script(script):
    # regular expression to identify  narrator
    narrator_pattern = r"Narrator: \"(.*?)\""
    narrator_pattern2 = r"Voiceover: \"(.*?)\""
    narrator_pattern3 = r"Host: \"(.*?)\""
    narrator_pattern4 = r"Narrator:\*\* \"(.*?)\""
    # converting tuple to string
    # narrator_pattern = "".join(narrator_pattern)

    # find narrator regex
    narrator_lines = re.findall(narrator_pattern, script)
    print("narrator")
    if narrator_lines == []:
        narrator_lines = re.findall(narrator_pattern2, script)
        print("voiceover")
    elif narrator_lines == []:
        narrator_lines = re.findall(narrator_pattern3, script)
        print("host")
    elif narrator_lines == []:
        narrator_lines = re.findall(narrator_pattern4, script)
        print("narrator**")

    print("wow", narrator_lines)

    # Replace the narrator lines in the script with an empty string to leave only other segments
    script_without_narrator = re.sub(narrator_pattern, "", script)

    # Split the remaining script by lines and filter out empty or whitespace-only lines
    other_segments = [
        line.strip() for line in script_without_narrator.splitlines() if line.strip()]

    # Return the separated lists
    return narrator_lines, other_segments
