# to be executed in src!!

import os
import json

def replace_other_content(string):
    with open("placeholders.json", "r") as f:
        placeholders = json.load(f)
    for ph in placeholders.keys():
        string = string.replace(ph, placeholders[ph])
    return string

total_n_posts = len(os.listdir("../posts"))
def fill_information_of_post(post, post_title, post_date, number_post):
    post = post.replace("{{post_title}}", post_title)
    post = post.replace("{{post_date}}", post_date)

    if 0 <= number_post - 1 <= total_n_posts - 1:
        post = post.replace("{{previous_post_link}}", str(number_post-1) + ".html")
    else:
        post = post.replace("{{previous_post_link}}", "")

    if 0 <= number_post + 1 <= total_n_posts - 1:
        post = post.replace("{{next_post_link}}", str(number_post-1) + ".html")
    else:
        post = post.replace("{{next_post_link}}", "")

    return post

# -------------------------------- MAKE INDEX ---------------------------------
# build post post_list
with open("components/post_entry.tem.html", "r") as f:
    post_entry_template = f.read()

to_insert = dict()
max_n_post = 0
for post_file in os.listdir("../posts"):
    post_properties = post_file.split("|")
    number_post = int(post_properties[0])
    if number_post > max_n_post:
        max_n_post = number_post
    post_date = post_properties[1] + " " + post_properties[2] + " " + post_properties[3]
    # .html has 5 characters
    post_title = post_properties[4][:-5]
    post_entry = post_entry_template.replace("{{post_title}}", post_title)
    post_entry = post_entry.replace("{{post_date}}", post_date)
    post_entry = post_entry.replace("{{post_link}}", post_properties[0] + ".html")

    # read post file, replace other content and copy outside folder
    with open("../posts/" + post_file, "r") as f:
        post_template = f.read()
    post = replace_other_content(post_template)
    post = fill_information_of_post(post, post_title, post_date, int(post_properties[0]))
    with open("../" + post_properties[0] + ".html", "w+") as f:
        f.write(post)

    to_insert[number_post] = post_entry

list_posts = ""
for i in range(max_n_post+1):
    list_posts += to_insert[i]

# now list_posts contains the lis to be inserted in index
with open("index.tem.html", "r") as f:
    index_template = f.read()

# make post list
index = index_template.replace("{{post_list}}", list_posts)
index = replace_other_content(index)
# write index
with open("../index.html", "w+") as f:
    f.write(index)

# ------------------- END MAKE INDEX ---------------------------------
