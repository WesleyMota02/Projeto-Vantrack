class VantrackException(Exception):
    """Exceção base para a aplicação"""
    pass

class UsuarioNaoEncontrado(VantrackException):
    pass

class EmailJaCadastrado(VantrackException):
    pass

class CPFJaCadastrado(VantrackException):
    pass

class SenhaInvalida(VantrackException):
    pass

class TokenInvalido(VantrackException):
    pass

class PermissaoNegada(VantrackException):
    pass

class DadosInvalidos(VantrackException):
    pass

class VeiculoNaoEncontrado(VantrackException):
    pass

class RotaNaoEncontrada(VantrackException):
    pass

class InscricaoNaoEncontrada(VantrackException):
    pass

class CapacidadeExcedida(VantrackException):
    pass

class DuplicacaoInscricao(VantrackException):
    pass

class LocalicaoGPSInvalida(VantrackException):
    pass
