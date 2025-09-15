import random
def main():
    french_words = [
        "arbre", "livre", "fleur", "plage", "chien", "table", "porte", "monde",
        "femme", "homme", "blanc", "noir", "frais", "doux", "grand", "petit",
        "point", "temps", "ville", "terre", "boisé", "bête", "loup", "tache",
        "choux", "calme", "bison", "liane", "plume", "crabe", "tordu",
        "ramer", "fumer", "fable", "bouse", "lisse", "rance", "farde", "piste",
        "jouer", "rêver", "chef", "taper", "usine", "style", "geste", "aimer", "clair"]

    selected_words = random.sample(french_words, 3)
    upper_words = [word.upper() for word in selected_words]
    print (selected_words)
    print("\n \n \n \n \n \n \n \n \n \n \n \n \n")
    print(selected_words[2])
    return upper_words


if __name__ == "__main__":
    main()
