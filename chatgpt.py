import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def structured_data(spending_text):

    syst = """
    Tu es un assistant intelligent de dépense. Je souhaite te donner une description de mes dépenses et je souhaite que tu transformes la description en format json avec les champs suivants.

    designation : la chose pour laquelle la dépense a été effectuée,
    moyen_paiement :  Le moyen de paiement dans la liste [Cash, mobile money ou Carte de crédit],
    categorie :  la catégorie de la dépense dans cette liste: 
    [transport, shopping, electricité, eau, loyer, voiture, television, sport, santé, loisirs, autres
    ]
    montant : le montant de la dépense

    Tu ne retournes que le format json. Aucun autre texte. Même pas "Voici la description de votre première dépense au format JSON
    """

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": syst},
            {"role": "user", "content": spending_text}, 
        ]
    )

    answer = response["choices"][0]['message']['content']

    return answer


def text_to_sql(question):

    syst = """
        J'ai une table SQL nommée "depenses" avec les colonnes suivantes :

            id INTEGER PRIMARY KEY,
            designation TEXT,
            moyen_paiement TEXT,
                categorie TEXT,
                montant REAL,
                date DATE,

            Transforme la question suivante en requête SQL qui répond à la question. Tu ne retournes que la requête SQL, aucun autre text introductif:
                

    """

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": syst},
            {"role": "user", "content": question}, 
        ]
    )

    answer = response["choices"][0]['message']['content']

    return answer

def reformule_answer(user_question, sql_result):

    syst = """
    En te basant sur le table SQL dont le schema est le
    suivant, génère une réponse en langage naturel  : 
    id INTEGER PRIMARY KEY,
        designation TEXT,
        moyen_paiement TEXT,
            categorie TEXT,
            montant REAL,
            date DATE
    """

    quest = f'''Voici la question qu'a posé l'utilisateur : 
    {user_question}
    La réponse : {sql_result}
    Si la réponse est un montant, l'unité monetaire est fcfa
    '''

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": syst},
            {"role": "user", "content": quest}, 
        ]
    )

    answer = response["choices"][0]['message']['content']

    return answer