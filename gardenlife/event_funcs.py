def update_garden_dropdown(window, gardens):
    garden_names = sorted(list(gardens))
    return window["-SELECT GARDEN-"].update(values=garden_names, size=(34, 10))


def clear_garden_values(window):
    for value in ("GARDEN NAME", "LOCATION", "SIZE", "OWNER NAMES", "OWNED SINCE"):
        window[f"-{value}-"].update("")


def clear_summary_values(window):
    for value in (
        "GARDEN NAME",
        "LOCATION",
        "SIZE",
        "OWNED BY",
        "OWNED FOR",
        "TOTAL CREATURES",
        "TOTAL PLANTS",
        "TOTAL TASKS",
        "OUTSTANDING TASKS",
    ):
        window[f"-SUMMARY {value}-"].update("")


def creature_instance(garden, values):
    return garden.creatures.get(values["-CREATURE NAME-"])


def update_creature_dropdowns(window, garden):
    creature_names = sorted([""] + list(garden.creatures))
    types = {c.org_type for c in garden.creatures.values() if c.org_type}
    creature_types = sorted([""] + list(types))
    return (
        window["-CREATURE NAME-"].update(values=creature_names, size=(25, 10)),
        window["-CREATURE TYPE-"].update(values=creature_types, size=(25, 10)),
    )


def clear_creature_values(window):
    for value in ("NAME", "TYPE", "APPEARED DATE", "STATUS", "NOTES"):
        window[f"-CREATURE {value}-"].update("")
    for value in ("IMPACT", "PREVALENCE", "TREND"):
        window[f"-CREATURE {value} SLIDER-"].update(3)


def plant_instance(garden, values):
    return garden.plants.get(values["-PLANT NAME-"])


def clear_plant_values(window):
    for value in ("NAME", "TYPE", "PLANTED DATE", "EDIBLE", "STATUS", "NOTES"):
        window[f"-PLANT {value}-"].update("")
    for value in ("IMPACT", "PREVALENCE", "TREND"):
        window[f"-PLANT {value} SLIDER-"].update(3)


def update_plant_dropdowns(window, garden):
    plant_names = sorted([""] + list(garden.plants))
    types = {p.org_type for p in garden.plants.values() if p.org_type}
    plant_types = sorted([""] + list(types))
    return (
        window["-PLANT NAME-"].update(values=plant_names, size=(25, 10)),
        window["-PLANT TYPE-"].update(values=plant_types, size=(25, 10)),
    )


def task_instance(garden, values):
    return garden.tasks.get(values["-TASK NAME-"])


def clear_task_values(window):
    for value in (
        "NAME",
        "PROGRESS",
        "NEXT DUE",
        "ASSIGNEE",
        "LENGTH",
        "STATUS",
        "NOTES",
        "START",
        "FREQUENCY",
        "COUNT",
        "BY MONTH",
        "INTERVAL",
    ):
        window[f"-TASK {value}-"].update("")
        task = None


def update_task_dropdown(window, garden):
    task_names = sorted([""] + list(garden.tasks))
    return window["-TASK NAME-"].update(values=task_names, size=(25, 10))


def clear_organism_links(window, garden):
    window["-TASK LINKED CREATURES-"].update(sorted(list(garden.creatures)))
    window["-TASK LINKED PLANTS-"].update(sorted(list(garden.plants)))


def update_all_item_dropdowns():
    update_creature_dropdowns()
    update_plant_dropdowns()
    update_task_dropdown()


def clear_all_item_dropdowns(window):
    for value in ("CREATURE NAME", "CREATURE TYPE", "PLANT NAME", "PLANT TYPE", "TASK NAME"):
        window[f"-{value}-"].update(values="", size=(25, 10))


def clear_all_item_values_and_links():
    clear_creature_values()
    clear_plant_values()
    clear_task_values()
    clear_organism_links()


def clear_all_values_and_links():
    clear_garden_values()
    clear_summary_values()
    clear_all_item_values_and_links()