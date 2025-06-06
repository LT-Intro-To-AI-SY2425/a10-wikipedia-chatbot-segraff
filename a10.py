import re, string, calendar
from wikipedia import WikipediaPage
import wikipedia
from bs4 import BeautifulSoup
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from match import match
from typing import List, Callable, Tuple, Any, Match


def get_page_html(title: str) -> str:
    """Gets html of a wikipedia page

    Args:
        title - title of the page

    Returns:
        html of the page
    """
    results = wikipedia.search(title)
    return WikipediaPage(results[0]).html()


def get_first_infobox_text(html: str) -> str:
    """Gets first infobox html from a Wikipedia page (summary box)

    Args:
        html - the full html of the page

    Returns:
        html of just the first infobox
    """
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all(class_="infobox")

    if not results:
        raise LookupError("Page has no infobox")
    return results[0].text


def clean_text(text: str) -> str:
    """Cleans given text removing non-ASCII characters and duplicate spaces & newlines

    Args:
        text - text to clean

    Returns:
        cleaned text
    """
    only_ascii = "".join([char if char in string.printable else " " for char in text])
    no_dup_spaces = re.sub(" +", " ", only_ascii)
    no_dup_newlines = re.sub("\n+", "\n", no_dup_spaces)
    return no_dup_newlines


def get_match(
    text: str,
    pattern: str,
    error_text: str = "Page doesn't appear to have the property you're expecting",
) -> Match:
    """Finds regex matches for a pattern

    Args:
        text - text to search within
        pattern - pattern to attempt to find within text
        error_text - text to display if pattern fails to match

    Returns:
        text that matches
    """
    p = re.compile(pattern, re.DOTALL | re.IGNORECASE)
    match = p.search(text)

    if not match:
        raise AttributeError(error_text)
    return match


def get_war_result(war_name: str) -> str:
    """Gets the result from a given war

    Args:
        war_name - name of the war to get result of

    Returns:
        result of the given war 
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(war_name)))
    pattern = r"(Result\s*(?P<result>[\w\s]*)Territorial)"
    error_text = "Page infobox has no result information"
    match = get_match(infobox_text, pattern, error_text)

    return match.group("result")


def get_president(name: str) -> str:
    """Gets the president of the number given 

    Args:
        number of the president 

    Returns:
        president name 
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(name)))
    pattern = r"\d{4}(?P<order>\d*\w{2})"

    error_text = (
        "Page infobox has no president order information (at least none in xxxx-xx-xx format)"
    )
    match = get_match(infobox_text, pattern, error_text)

    return match.group("order")

def get_everything(thing: str) -> str:
    infobox_text = clean_text(get_first_infobox_text(get_page_html(thing)))
    return infobox_text

def get_president_birthday(entity_name: str) -> str:
    """Gets the presidents birth day of a president from its Wikipedia infobox.

    Args:
        presdient name
    Returns:
        birthday of president
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(entity_name)))

    # Regex pattern to match scientific name in binomial nomenclature
    pattern = r"(?P<birthday>\d{4}-\d{2}-\d{2})"
    error_text = "Page infobox has no president birthday information"
    match = get_match(infobox_text, pattern, error_text)

    birthday = match.group('birthday').strip()
    return f"President's birthday {birthday}"

def get_founding(entity_name: str) -> str:
    """Gets the year a city was founded.

    Args:
        entity_name: Name of the city.

    Returns:
        year the city was founded
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(entity_name)))

    # Regex pattern to match conservation status, often found under "Conservation status"
    pattern = r"((City\sstatus)|(Settled(c. )?))(?P<found>(\w+ \d+, )?\d{4})"
    error_text = "Page infobox has no founding information"
    match = get_match(infobox_text, pattern, error_text)

    found = match.group('found').strip()
    return f"Founded: {found}"

def get_happen(entity_name: str) -> str:
    """Gets the year a historical event happened from its Wikipedia infobox.

    Args:
        entity_name: historical event 

    Returns: year of event 
        
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(entity_name)))

    # Regex pattern to match conservation status, often found under "Conservation status"
    pattern = r"Location\s?(?P<happen>\w+)"
    error_text = "Page infobox has no domain information"
    match = get_match(infobox_text, pattern, error_text)

    happen = match.group('happen').strip()
    return f"Location: {happen}"

def get_first_lady(entity_name: str) -> str:
    """Gets the first lady of a president from its Wikipedia infobox.

    Args:
        presdient name
    Returns:
        first lady 
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(entity_name)))

    # Regex pattern to match scientific name in binomial nomenclature
    pattern = r"Spouse[\n\s](?P<first_lady>\w* \w*)"
    error_text = "Page infobox has no president birthday information"
    match = get_match(infobox_text, pattern, error_text)

    the_first_lady = match.group('first_lady').strip()
    return f"First Lady: {the_first_lady}"
        





# below are a set of actions. Each takes a list argument and returns a list of answers
# according to the action and the argument. It is important that each function returns a
# list of the answer(s) and not just the answer itself.


def president(matches: List[str]) -> List[str]:
    """Returns president of the number in matches

    Args:
        matches - match from pattern of number given to find president

    Returns:
        president name
    """
    return [get_president(" ".join(matches))]


def war_result(matches: List[str]) -> List[str]:
    """Returns war result of war in matches

    Args:
        matches - match from pattern of war to find result of

    Returns:
        result of war
    """
    return [get_war_result(matches[0])]

def everything(matches: List[str]) -> List[str]:
    return [get_everything(matches[0])]

def president_name(matches: List[str]) -> List[str]:
    """Returns the scientific name of a given animal.

    Args:
        matches - match from pattern for animal to find scientific name 

    Returns:
        Birthday of the president
    """
    return [get_president_birthday(" ".join(matches))]

def founding(matches: List[str]) -> List[str]:
    """Returns the year a given city was founded
    Args:
        matches - match from pattern for animal to find given conservation status

    Returns:
        Conservation status of animal
    """
    return [get_founding(" ".join(matches))]

def happen(matches: List[str]) -> List[str]:
    """Returns the conservation status of a given animal.

    Args:
        matches - match from pattern for animal to find given conservation status

    Returns:
        Conservation status of animal
    """
    return [get_happen(" ".join(matches))]

def first_lady(matches: List[str]) -> List[str]:
    """Returns the scientific name of a given animal.

    Args:
        matches - match from pattern for animal to find scientific name 

    Returns:
        Birthday of the president
    """
    return [get_first_lady(" ".join(matches))]

# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# type aliases to make pa_list type more readable, could also have written:
# pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [...]
Pattern = List[str]
Action = Callable[[List[str]], List[Any]]

# The pattern-action list for the natural language query system. It must be declared
# here, after all of the function definitions
pa_list: List[Tuple[Pattern, Action]] = [
    ("which number president was %".split(), president),
    ("what was the result of the %".split(), war_result),
    ("when was the birthday of %".split(), president_name),
    ("when was the founding of %".split(), founding),
    ("tell me everything about %".split(), everything),
    ("what was the location of %".split(), happen),
    ("who was the first lady of %".split(), first_lady )
    (["bye"], bye_action),
]


def search_pa_list(src: List[str]) -> List[str]:
    """Takes source, finds matching pattern and calls corresponding action. If it finds
    a match but has no answers it returns ["No answers"]. If it finds no match it
    returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches and
        ["No answers"] if it finds a match but no answers
    """
    for pat, act in pa_list:
        mat = match(pat, src)
        if mat is not None:
            answer = act(mat)
            return answer if answer else ["No answers"]

    return ["I don't understand"]


def query_loop() -> None:
    """The simple query loop. The try/except structure is to catch Ctrl-C or Ctrl-D
    characters and exit gracefully"""
    print("Welcome to the Wikipedia database!\n")

    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nSo long!\n")




# uncomment the next line once you've implemented everything are ready to try it out
query_loop()