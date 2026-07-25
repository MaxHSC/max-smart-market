from server.database import user_dao


class AuthenticationActions:
    def __init__(self) -> None:
        self.acess_mapping = {
            "checkDocumentNewUser":self.check_document_new_user,
            "inserDataNewUser":self.insert_data_new_user,
        }
        self.type_user_list = [
            "CLIENTE","GERENTE","COLABORADOR"
        ]



    def check_document_new_user(self,document: str, phone_login: str) -> bool: #PRIMEIRA DE 3 ETAPAS PARA CADASTROS DE USER - VERIFICAR SE CPF E TELEFONE ESTÃO CADASTRADOS
        try:
            if len(document) != 11:
                raise ValueError
            
            if not document.isdigit():
                raise TypeError
            
            check_document = user_dao.check_document_already_exists(document)

            if check_document:
                return check_document

            if len(phone_login) != 11:
                raise ValueError
                        
            if not phone_login.isdigit():
                raise TypeError

            check_phone = user_dao.check_phone_already_exists(phone_login)

            return check_phone
        
        except (TypeError,ValueError):
            print(f"\n[BANCO DE DADOS - CADASTRO] CAMPO INFORMADO INVÁLIDO.\n")
            return False


    def insert_data_new_user(self,username: str, document: str, phone_number: str, pass_key: str, type_user: str) -> bool: #SEGUNDA DE 3 ETAPAS PARA CADASTROS DE USER - INSERIR AS INFORMAÇÕES NO DB
        if type_user not in self.type_user_list:
            print(f"\n[BANCO DE DADOS - CADASTRO] CADASTRO DE USUÁRIO NÃO PERMITIDO.\n")
            return False

        add_new_user = user_dao.new_user(username,document,phone_number,pass_key,type_user)

        return add_new_user

    #TERCEIRA DE 3 ETAPAS PARA CADASTROS DE USER - CONFIRMAR TELEFONE COM SMS OU WHATSAPP

    def confirm_login(self,phone_login: str, pass_key: str):
        try:
            if len(phone_login) != 11:
                raise ValueError
                        
            if not phone_login.isdigit():
                raise TypeError

            login_result = user_dao.confirm_login_user(phone_login,pass_key)

            session = True

            return login_result, session

        except (TypeError,ValueError):
            print(f"\n[BANCO DE DADOS - LOGIN] CAMPO INFORMADO INVÁLIDO.\n")
            return False