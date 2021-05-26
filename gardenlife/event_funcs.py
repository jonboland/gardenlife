from datetime import datetime


def check_date_validity(date):
    return datetime.strptime(date, "%d/%m/%Y")


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


def update_task_dropdown(window, garden):
    task_names = sorted([""] + list(garden.tasks))
    return window["-TASK NAME-"].update(values=task_names, size=(25, 10))


def clear_organism_links(window, garden):
    window["-TASK LINKED CREATURES-"].update(sorted(list(garden.creatures)))
    window["-TASK LINKED PLANTS-"].update(sorted(list(garden.plants)))


def update_all_item_dropdowns(window, garden):
    update_creature_dropdowns(window, garden)
    update_plant_dropdowns(window, garden)
    update_task_dropdown(window, garden)


def clear_all_item_dropdowns(window):
    for value in (
        "CREATURE NAME",
        "CREATURE TYPE",
        "PLANT NAME",
        "PLANT TYPE",
        "TASK NAME",
    ):
        window[f"-{value}-"].update(values="", size=(25, 10))


def clear_all_item_values_and_links(window, garden):
    clear_creature_values(window)
    clear_plant_values(window)
    clear_task_values(window)
    clear_organism_links(window, garden)


def clear_all_values_and_links(window, garden):
    clear_garden_values(window)
    clear_summary_values(window)
    clear_all_item_values_and_links(window, garden)
    