def change_stylesheet(parent_widget=None, obj_name=None, **kwargs):
    # Find target selector and Crop Stylesheet
    stylesheet = parent_widget.styleSheet()
    if obj_name[0] == "Q":
        start = stylesheet.find("".join([obj_name, " ", "{"]))
    else:
        start = stylesheet.find("".join(["#", obj_name, " ", "{"]))
    end = start + stylesheet[start:].find("}")
    crop_stylesheet = stylesheet[start:end]

    # Change stylesheet by kwargs
    for key, value in kwargs.items():
        key = key.replace("_", "-")
        new_start = crop_stylesheet.find("\n" + str(key) + ":") + 1
        new_end = new_start + crop_stylesheet[new_start:].find(";") + 1

        new_css = "".join([key, ": ", value, ";"])

        if new_start != 0:
            # print(f"  [Info] {obj_name}'s css has changed from:{crop_stylesheet[new_start:new_end]} -> to:{new_css})")
            if value != "del":
                stylesheet = "".join([stylesheet[:start],
                                      crop_stylesheet[:new_start],
                                      new_css,
                                      crop_stylesheet[new_end:],
                                      stylesheet[end:]])
            elif value == "del":
                stylesheet = "".join([stylesheet[:start],
                                      crop_stylesheet[:new_start],
                                      crop_stylesheet[new_end:],
                                      stylesheet[end:]])

        else:
            stylesheet = "".join([stylesheet[:start],
                                  crop_stylesheet,
                                  new_css,
                                  crop_stylesheet[new_end:],
                                  stylesheet[end:]])

        stylesheet = stylesheet.replace("\n\n", "\n")

    return stylesheet