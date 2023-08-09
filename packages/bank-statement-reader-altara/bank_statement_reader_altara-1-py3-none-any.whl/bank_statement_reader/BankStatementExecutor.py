from bank_statement_reader.AccessBankStatement import AccessBankStatement
from bank_statement_reader.FcmbBankStatement import FcmbBankStatement
from bank_statement_reader.FidelityBankStatement import FidelityBankStatement
from bank_statement_reader.FirstBankStatement import FirstBankStatement
from bank_statement_reader.GtBankStatement import GtBankStatement
from bank_statement_reader.SterlingBankStatement import SterlingBankStatement
from bank_statement_reader.UBABankStatement import UBABankStatement
from bank_statement_reader.ZenithBankStatement import ZenithBankStatement


class BankStatementExecutor:
    BANK_STATEMENTS_CHOICES = {
        1: "Zenith",
        2: "UBA",
        3: "Access",
        4: "First",
        5: "GT",
        6: "FCMB",
        7: "Fidelity",
        8: "Sterling"
        # Add more bank statements with corresponding numbers here
    }

    def __init__(self):
        # self.pdf_directory = pdf_directory
        self.bank_statements = self.BANK_STATEMENTS_CHOICES

    def close(self):
        exit(0)

    def display_menu(self):
        print("Available Bank Statements:")
        for number, statement in self.bank_statements.items():
            print(f"{number}. {statement}")

    def get_user_choice(self):
        while True:
            try:
                choice = int(input("Select a number to execute the corresponding bank statement: "))
                if choice in self.bank_statements:
                    return choice
                else:
                    print("Invalid option. Please choose a valid number.")
            except ValueError:
                self.display_menu()
                print("Invalid input. Please enter a number.")

    def execute(self, choice, pdf_file='', password=''):
        try:
            file_to_execute = self.bank_statements.get(choice)
            print(file_to_execute + " Bank Statement Selected")
            module_name = file_to_execute + "BankStatement.py"
            class_name = self.bank_statements[choice] + "BankStatement"
            bank_statement = None
            if choice == 1:
                bank_statement = ZenithBankStatement(pdf_file)
            elif choice == 2:
                bank_statement = UBABankStatement(pdf_file)
            elif choice == 3:
                bank_statement = AccessBankStatement(pdf_file)
            elif choice == 4:
                bank_statement = FirstBankStatement(pdf_file, password)
            elif choice == 5:
                bank_statement = GtBankStatement(pdf_file)
            elif choice == 6:
                bank_statement = FcmbBankStatement(pdf_file)
            elif choice == 7:
                bank_statement = FidelityBankStatement(pdf_file)
            elif choice == 8:
                bank_statement = SterlingBankStatement(pdf_file)
            result = bank_statement.result()
            excel_file_path = bank_statement.export_to_excel(
                dataframe=result.get('dataframe'),
                name=result.get('account_name'),
                start_date=result.get('period').get('from_date'),
                end_date=result.get('period').get('to_date')
            )
            result.pop('dataframe')
            if excel_file_path:
                result.update({'excel_file': excel_file_path})
            return result
        except Exception as e:

            raise Exception("Invalid option. Unable to execute the selected bank statement.")


if __name__ == "__main__":
    executor = BankStatementExecutor()
    # executor.display_menu()
    # choice = executor.get_user_choice()
    response = executor.execute(2)
    print(response)

print("From import")
