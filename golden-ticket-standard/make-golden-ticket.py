import re
import printing as p

def main ():
    done = p.ask("Is this moving to Done? y/n")
    done = done.lower()
    if done != 'y':
        nwr = p.ask("Is this a 'No work required'? y/n")
        if nwr != 'y':
            p.err("If it's not 'Done' or 'No work required', idk what you're on.")
            return
        comment = get_nwr_comment()
    else:
        comment = get_done_comment()
    if comment == "":
        return
    comment = comment.rstrip()
    p.info("=====  START  =====")
    p.info("")
    p.info(comment)
    p.info("")
    p.info("=====   END   =====")

def get_done_comment ():
    fix_version = p.ask("What version was this fixed in?")
    fix_version = fix_version.upper()
    if fix_version[0] != "V":
        fix_version = "V" + fix_version
    if not validate_version(fix_version): 
        p.ask("Please enter a proper fix version.")
        if not validate_version(fix_version):
            p.err("Tell me what version it was fixed in, you spudnugget.")
            return ""
    user_info = p.ask("What was wrong? (For dummies)")
    support_info = p.ask("Any support notes?")
    dev_notes = p.ask("Any dev notes?")
    cherry_pick_info = p.ask("Cherry-picking notes? [Standard 48hrs]")

    if is_no(cherry_pick_info):
        cherry_pick_info = "Standard 48hrs"

    comment = add_to_comment("", "Fixed in Version", fix_version)
    comment = add_to_comment(comment, "User-targeted Info", user_info)
    comment = add_to_comment(comment, "Frontline Info", support_info)
    comment = add_to_comment(comment, "Dev Info", dev_notes)
    comment = add_to_comment(comment, "Cherry-Picking", cherry_pick_info)

    return comment    

def get_nwr_comment ():
    reason = p.ask("Why doesn't this require work? O_o")
    support_info = p.ask("Got any more information to help support?")
    
    comment = add_to_comment("", "Reasoning", reason)
    comment = add_to_comment(comment, "Next steps for the frontline", support_info)
    
    return comment

def validate_version (version):
    return (not is_no(version) and re.match(r"V[0-9]{1,3}\.[0-9]+", version)) 

def add_to_comment (comment, section, info):
    if is_no(info):
        info = "N/A"
    new_comment = comment + "*" + section + ":* " + info + "\n"
    return new_comment

def is_no (string):
    string = string.lower()
    re.sub(r'\W+', '', string)
    return string == "" or string == "n" or string == "no" or string == "none" or string == "na" or string == "nah" or string == "nope" or string == "not really"

# Then connect to Jira, execute the transaction, and add the comment in

# Initially, we want to do this as a command line thing, but then maybe add a UI? Sounds like work though...

main()
