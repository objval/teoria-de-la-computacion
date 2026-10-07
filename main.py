"""
test_lexer.py
Suite de pruebas unitarias para el analizador lexico de Prolog.
Asignatura: Teoria de la Computacion (INFO1148).
"""

import os
import sys
import unittest

# Permite ejecutar los tests directamente desde la raiz o dentro de tests/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import Lexer, Token


class BaseLexerTest(unittest.TestCase):
    """Clase base con metodos auxiliares para simplificar aserciones."""

    def obtener_tokens(self, codigo_fuente):
        lexer = Lexer(codigo_fuente)
        tokens = lexer.tokenize()
        # Retornamos solo (tipo, lexema) para evaluar reconocimiento directo
        return [(t.tipo, t.lexema) for t in tokens], lexer.errors


# =========================================================================
# 1. CASOS DE PRUEBA VALIDOS (Al menos 20 pruebas requeridas)
# =========================================================================
class TestCasosValidos(BaseLexerTest):

    def test_01_atomo_simple(self):
        tokens, errors = self.obtener_tokens("padre persona_1 animal")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("ATOMO", "padre"),
                ("ATOMO", "persona_1"),
                ("ATOMO", "animal"),
            ],
        )

    def test_02_atomo_entrecomillado(self):
        tokens, errors = self.obtener_tokens("'Juan Perez' 'consulta rapida'")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("ATOMO", "'Juan Perez'"),
                ("ATOMO", "'consulta rapida'"),
            ],
        )

    def test_03_atomo_entrecomillado_con_escapes(self):
        tokens, errors = self.obtener_tokens(r"'O\'Connor' 'salto\nlinea'")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("ATOMO", r"'O\'Connor'"),
                ("ATOMO", r"'salto\nlinea'"),
            ],
        )

    def test_04_variable_estandar(self):
        tokens, errors = self.obtener_tokens("X Persona Total_Final")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("VAR", "X"),
                ("VAR", "Persona"),
                ("VAR", "Total_Final"),
            ],
        )

    def test_05_variable_prefijo_guion_bajo(self):
        tokens, errors = self.obtener_tokens("_Temp _123 _resultado")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("VAR", "_Temp"),
                ("VAR", "_123"),
                ("VAR", "_resultado"),
            ],
        )

    def test_06_variable_anonima(self):
        tokens, errors = self.obtener_tokens("_ _ _")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("VAR_ANON", "_"),
                ("VAR_ANON", "_"),
                ("VAR_ANON", "_"),
            ],
        )

    def test_07_numeros_enteros(self):
        tokens, errors = self.obtener_tokens("0 42 2026")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("NUM_INT", "0"),
                ("NUM_INT", "42"),
                ("NUM_INT", "2026"),
            ],
        )

    def test_08_numeros_reales(self):
        tokens, errors = self.obtener_tokens("3.1415 0.5 100.001")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("NUM_REAL", "3.1415"),
                ("NUM_REAL", "0.5"),
                ("NUM_REAL", "100.001"),
            ],
        )

    def test_09_numeros_reales_notacion_cientifica(self):
        tokens, errors = self.obtener_tokens("1.2e-3 5.0E+2 3.14e10")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("NUM_REAL", "1.2e-3"),
                ("NUM_REAL", "5.0E+2"),
                ("NUM_REAL", "3.14e10"),
            ],
        )

    def test_10_cadenas_doble_comilla(self):
        tokens, errors = self.obtener_tokens('"Hola mundo" "Prolog 2026"')
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("CADENA", '"Hola mundo"'),
                ("CADENA", '"Prolog 2026"'),
            ],
        )

    def test_11_cadenas_con_escapes(self):
        tokens, errors = self.obtener_tokens(r'"Texto con \"comillas\" y \n"')
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("CADENA", r'"Texto con \"comillas\" y \n"'),
            ],
        )

    def test_12_operadores_de_clausulas(self):
        tokens, errors = self.obtener_tokens(":- ?- -->")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("OP_CLAUS", ":-"),
                ("OP_CLAUS", "?-"),
                ("OP_CLAUS", "-->"),
            ],
        )

    def test_13_operadores_unificacion_y_comparacion(self):
        tokens, errors = self.obtener_tokens("= \\= == \\== =..")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("OP_COMP", "="),
                ("OP_COMP", "\\="),
                ("OP_COMP", "=="),
                ("OP_COMP", "\\=="),
                ("OP_COMP", "=.."),
            ],
        )

    def test_14_operadores_relacionales(self):
        tokens, errors = self.obtener_tokens("< =< > >=")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("OP_COMP", "<"),
                ("OP_COMP", "=<"),
                ("OP_COMP", ">"),
                ("OP_COMP", ">="),
            ],
        )

    def test_15_operadores_aritmeticos_simbolos(self):
        tokens, errors = self.obtener_tokens("+ - * / // **")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("OP_ARIT", "+"),
                ("OP_ARIT", "-"),
                ("OP_ARIT", "*"),
                ("OP_ARIT", "/"),
                ("OP_ARIT", "//"),
                ("OP_ARIT", "**"),
            ],
        )

    def test_16_operadores_aritmeticos_palabras(self):
        tokens, errors = self.obtener_tokens("X is Y mod 2")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("VAR", "X"),
                ("OP_ARIT", "is"),
                ("VAR", "Y"),
                ("OP_ARIT", "mod"),
                ("NUM_INT", "2"),
            ],
        )

    def test_17_operadores_control(self):
        tokens, errors = self.obtener_tokens("\\+ ! ; ,")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("OP_CTRL", "\\+"),
                ("OP_CTRL", "!"),
                ("OP_CTRL", ";"),
                ("OP_CTRL", ","),
            ],
        )

    def test_18_delimitadores_y_puntuacion(self):
        tokens, errors = self.obtener_tokens("( ) [ ] { } | .")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("DELIM", "("),
                ("DELIM", ")"),
                ("DELIM", "["),
                ("DELIM", "]"),
                ("DELIM", "{"),
                ("DELIM", "}"),
                ("DELIM", "|"),
                ("DELIM", "."),
            ],
        )

    def test_19_comentario_linea_ignorado(self):
        codigo = "% Comentario inicial\npadre(juan). % Comentario final"
        tokens, errors = self.obtener_tokens(codigo)
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("ATOMO", "padre"),
                ("DELIM", "("),
                ("ATOMO", "juan"),
                ("DELIM", ")"),
                ("DELIM", "."),
            ],
        )

    def test_20_comentario_bloque_multilinea(self):
        codigo = "padre /* este es un comentario\n   de bloque multilinea */ (juan)."
        tokens, errors = self.obtener_tokens(codigo)
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("ATOMO", "padre"),
                ("DELIM", "("),
                ("ATOMO", "juan"),
                ("DELIM", ")"),
                ("DELIM", "."),
            ],
        )


# =========================================================================
# 2. CASOS DE MÁXIMA COINCIDENCIA (MAXIMAL MUNCH) Y PRIORIDADES
# =========================================================================
class TestMaximaCoincidenciaYPrioridades(BaseLexerTest):

    def test_prioridad_desigualdad_estricta_frente_a_prefijos(self):
        # \== no debe separarse en \= y =
        tokens, errors = self.obtener_tokens("A \\== B")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens, [("VAR", "A"), ("OP_COMP", "\\=="), ("VAR", "B")]
        )

    def test_prioridad_operador_univoco(self):
        # =.. no debe separarse en = y ..
        tokens, errors = self.obtener_tokens("Term =.. Lista")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens, [("VAR", "Term"), ("OP_COMP", "=.."), ("VAR", "Lista")]
        )

    def test_variable_anonima_frente_a_variable_nombrada(self):
        # _ aislado es anónima; _Var es variable regular
        tokens, errors = self.obtener_tokens("_ _Temp")
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens, [("VAR_ANON", "_"), ("VAR", "_Temp")])

    def test_operador_clausula_frente_a_dos_puntos(self):
        tokens, errors = self.obtener_tokens("cuerpo :- regla.")
        self.assertEqual(len(errors), 0)
        self.assertEqual(
            tokens,
            [
                ("ATOMO", "cuerpo"),
                ("OP_CLAUS", ":-"),
                ("ATOMO", "regla"),
                ("DELIM", "."),
            ],
        )


# =========================================================================
# 3. CASOS DE PRUEBA INVÁLIDOS Y RECUPERACIÓN (Al menos 8 requeridos)
# =========================================================================
class TestCasosInvalidosYErrores(BaseLexerTest):

    def test_err_01_atomo_sin_cierre_en_linea(self):
        codigo = "'atomo abierto\npadre(ana)."
        tokens, errors = self.obtener_tokens(codigo)
        self.assertGreaterEqual(len(errors), 1)
        # Verifica recuperación y lectura del resto del código
        self.assertTrue(any("sin cerrar" in err.lower() for err in errors))
        self.assertIn(("ATOMO", "padre"), tokens)

    def test_err_02_cadena_sin_cierre(self):
        codigo = '"cadena sin fin\nX = 1.'
        tokens, errors = self.obtener_tokens(codigo)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("cadena" in err.lower() for err in errors))
        self.assertIn(("VAR", "X"), tokens)

    def test_err_03_comentario_bloque_sin_cierre(self):
        codigo = "padre(juan). /* comentario que nunca cierra hasta eof"
        tokens, errors = self.obtener_tokens(codigo)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("comentario" in err.lower() for err in errors))
        self.assertEqual(tokens[0], ("ATOMO", "padre"))

    def test_err_04_caracter_no_admitido_pesos(self):
        codigo = "total = $100."
        tokens, errors = self.obtener_tokens(codigo)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("$" in err for err in errors))
        # Debe recuperarse y registrar el 100
        self.assertIn(("NUM_INT", "100"), tokens)

    def test_err_05_caracter_no_admitido_arroba(self):
        codigo = "usuario@correo"
        tokens, errors = self.obtener_tokens(codigo)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("@" in err for err in errors))
        self.assertIn(("ATOMO", "usuario"), tokens)
        self.assertIn(("ATOMO", "correo"), tokens)

    def test_err_06_caracter_no_admitido_tilde(self):
        codigo = "valor ~ 45."
        tokens, errors = self.obtener_tokens(codigo)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("~" in err for err in errors))
        self.assertIn(("NUM_INT", "45"), tokens)

    def test_err_07_numero_mal_formado_punto_sin_decimal(self):
        # '12.alpha' no es real válido en Prolog; debe reportar error o separar correctamente
        codigo = "12.alpha"
        tokens, errors = self.obtener_tokens(codigo)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("12." in err or "formato" in err.lower() for err in errors))

    def test_err_08_numero_exponente_sin_digitos(self):
        codigo = "1.5e+ valor."
        tokens, errors = self.obtener_tokens(codigo)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("exponente" in err.lower() or "formato" in err.lower() for err in errors))


# =========================================================================
# 4. REGISTRO DE POSICIONES (Línea y Columna)
# =========================================================================
class TestPosiciones(unittest.TestCase):

    def test_posicion_linea_y_columna(self):
        codigo = "padre(\n  juan\n)."
        lexer = Lexer(codigo)
        tokens = lexer.tokenize()

        # Verifica tupla canónica <tipo, lexema, linea, columna>
        # 'padre' -> L1, C1
        self.assertEqual((tokens[0].tipo, tokens[0].linea, tokens[0].columna), ("ATOMO", 1, 1))
        # 'juan' -> L2, C3
        self.assertEqual((tokens[2].tipo, tokens[2].linea, tokens[2].columna), ("ATOMO", 2, 3))
        # '.' -> L3, C2
        self.assertEqual((tokens[4].tipo, tokens[4].linea, tokens[4].columna), ("DELIM", 3, 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)