from flask import Flask, render_template, request
from itertools import permutations, combinations, combinations_with_replacement, product
import math

app = Flask(__name__)

def calculate_total_count(n, r, calculation_type):
    """ Calcola solo il numero totale di permutazioni, disposizioni o combinazioni. """
    if calculation_type == "permutations":
        return math.factorial(n) // math.factorial(n - r)  # P(n, r) = n! / (n-r)!
    elif calculation_type == "dispositions_no_repetition":
        return math.factorial(n) // math.factorial(n - r)  # Uguale a P(n, r)
    elif calculation_type == "dispositions_with_repetition":
        return n ** r  # D(n, r) = n^r
    elif calculation_type == "combinations_no_repetition":
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))  # C(n, r) = n! / (r!(n-r)!)
    elif calculation_type == "combinations_with_repetition":
        return math.factorial(n + r - 1) // (math.factorial(r) * math.factorial(n - 1))  # C(n+r-1, r)
    return 0

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    
    if request.method == "POST":
        num_objects = request.form.get("num_objects")
        objects_list = request.form.get("objects_list")
        combinations_number = request.form.get("combinations_number")
        calculation_type = request.form.get("calculation_type")
        only_count = request.form.get("only_count")  # Checkbox per mostrare solo il numero totale

        # Verifica che solo uno tra num_objects e objects_list sia valorizzato
        if num_objects and objects_list:
            error = "Errore: inserire solo uno dei due campi (numero degli oggetti o lista)."
        
        elif num_objects:  # Se l'utente inserisce solo il numero
            try:
                n = int(num_objects)
                r = int(combinations_number)
                total_count = calculate_total_count(n, r, calculation_type)
                result = {"total_text": f"Numero totale di combinazioni: {total_count}", "combinations": []}
            except ValueError:
                error = "Errore: Inserire valori numerici validi."
        
        elif objects_list:  # Se l'utente inserisce una lista di oggetti
            objects_list = objects_list.split(",")  # Converti la stringa in lista
            num_objects = len(objects_list)  # Calcola n in base alla lista

            try:
                r = int(combinations_number)
                if only_count:  # Se l'utente ha selezionato "Solo numero totale"
                    total_count = calculate_total_count(num_objects, r, calculation_type)
                    result = {"total_text": f"Numero totale delle sequenze: {total_count}", "combinations": []}
                else:
                    # Calcola le combinazioni o permutazioni in base al tipo selezionato
                    if calculation_type == "permutations":
                        raw_result = list(permutations(objects_list, r))
                    elif calculation_type == "dispositions_no_repetition":
                        raw_result = list(permutations(objects_list, r))
                    elif calculation_type == "dispositions_with_repetition":
                        raw_result = list(product(objects_list, repeat=r))
                    elif calculation_type == "combinations_no_repetition":
                        raw_result = list(combinations(objects_list, r))
                    elif calculation_type == "combinations_with_repetition":
                        raw_result = list(combinations_with_replacement(objects_list, r))

                    # Formattazione della lista in stringhe pulite, separando gli oggetti con uno spazio
                    formatted_result = [" ".join(item) for item in raw_result]

                    # Conta il numero totale delle combinazioni
                    total_count = len(raw_result)
                    
                    # Crea il testo per il numero totale di combinazioni
                    result_text = f"Numero totale delle sequenze: {total_count}"
                    
                    # Manteniamo la lista delle combinazioni
                    result = {"total_text": result_text, "combinations": formatted_result}

            except ValueError:
                error = "Errore: Inserire valori validi."

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)

