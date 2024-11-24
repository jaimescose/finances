# Finances

Personal repo to keep track of my finances. Therefore, the following isntructions are just a reminder for myself.

I keep track of my expenses and incomes using [Zumma](https://www.zummafinancial.com/).
Althouhgh, it might lack of some functionalties (even for me), it's a simple enough (to not give up setting up), and moreover, it has a WhatsApp bot that you could type transactions in natural language and it will do a decent job to tag it with the right category and other relavant information (so you don't lost consistency because you need to enter the information manually).

## How to use it

1. Go to Zumma -> "Perfil" -> "Descargas" -> "Historial de gastos e ingresos"
2. A file will be sent to my personal email and labeled as "Finances/movimientos"
3. Then, a Zapier automation will download the file and place it in a Google Drive folder (`G:\My Drive\life\finance\movimientos`)
4. Copy the file in the same folder and rename it to "actividades.csv" (I do this just to keep the original file, so I don't need to download it again if something goes wrong)
5. Then, within this repo, run `uv run main.py`
6. Copy and paste the contents from the output files as follows (this steo could be automated in the future connecting the script directly to my Google workspace):
    - `expenses.xlsx` content paste in "Gastos" sheet of your Google Sheets file
    - `incomes.xlsx` content paste in "_ingresos" sheet of your Google Sheets file
