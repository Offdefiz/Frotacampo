import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkcalendar import Calendar
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import pytesseract
from tkinter import font
from PIL import ImageFont, ImageTk, ImageDraw
import autocombobox
from tkinter import messagebox

# Dicionário de estados e suas respectivas cidades
estados = {
    
    "Minas Gerais": [ "Belo Horizonte", "Contagem", "Betim", "Ibirité", "Santa Luzia",
                    "Sabará", "Ribeirão das Neves", "Nova Lima", "Lagoa Santa", "Vespasiano",
                    "Sarzedo", "Mário Campos", "Rio Acima", "Brumadinho", "Caeté",
                    "Conselheiro Lafaiete", "Barbacena", "Itabira", "Itaúna", "Sete Lagoas",
                    "São João Nepomuceno", "Curvelo", "João Monlevade", "Montes Claros", "Governador Valadares" ],

       "São Paulo": ["Americana", "Campinas", "Capivari", "Hortolândia", "Itatiba", 
                    "Jundiaí", "Mogi das Cruzes", "Caçapava", "Guaratingueta", "Guararema", "Santa Isabel", 
                    "São José dos Campos", "Taubaté", "Lorena", "Cruzeiro", "Norte", "Sul", "Leste", "Oeste",
                    "Osasco", "Guarulhos", "ABCD", "Santo Andre", "São Bernardo", "São Caetano", "Diadema", 
                    "Barueri", "Santos", "Praia Grande", "Cubatão", "Itanhaem", "Peruibe", "Mongagua", "São Vicente", 
                    "Bertioga", "Guarujá", "São Sebastião", "Ubatuba", "Caraguatatuba", "Ilha-Bela", "Itu", "Indaiatuba", 
                    "Mairinque", "Salto", "São Roque", "Sorocaba", "Campos dos Jordão", "São Bento do Sapucai", "Atibaia", 
                    "Bragança Paulista", "Aguas de Lindoia", "Socorro", "Jaguariuna", "Holambra", "São Lourenço da Serra", 
                    "Juquitiba", "Miracatu", "Juquia", "Registro", "Pariquera-açu", "Iguape", "Ilha Comprida"],

    "Rio de Janeiro": ["Rio de Janeiro", "Niteroi", "São Gonçalo", "Duque de Caxias", "Nilopolis",
                    "Mesquita", "Nova Iguaçu", "SJ de Meriti", "Belford Roxo", "Itaborai (Centro)",
                    "Magé", "Queimados", "Japeri", "Itaguai (Centro)", "Seropédica",
                    "Barra do Pirai", "Vassouras", "Valença", "Miguel Pereira", "Paty do Alferes",
                    "Eng. Paulo de Frontin", "Mendes", "Paracambi", "Pirai", "Pinheral",
                    "Volta Redonda", "Barra Mansa", "Porto Real", "Quatis", "Resende",
                    "Itatiaia", "Mangaratiba", "Angra dos Reis", "Itaguai (além do centro)", "Paraty",
                    "Marica", "Saquarema", "Araruama", "Iguaba", "S.P. da Aldeia",
                    "Cabo Frio", "Buzios", "Arraial do Cabo", "Rio das Ostras", "Macaé",
                    "Silva Jardim", "Casimiro de Abreu", "Itaborai (além do centro)", "Tangua", "Tres Rios",
                    "Petropolis", "Teresópolis", "Nova Friburgo (Lumiar e S.P. da Serra quinzenal)", "Guapimirim", "Cachoeiras de Macacu",
                    "Sumidouro", "Duas Barras", "Bom Jardim", "Cordeiro", "Macuco",
                    "Cantagalo", "Trajano de Morais", "Carmo"],

    "Espírito Santo": ["Vitória", "Vila Velha", "Serra"],

    "São Paulo-Bauru": ["Bauru", "Agudos", "Piratininga", "Arealva", "Iacanga", 
                    "Avaí", "Pirajuí", "Guaranta", "Cafelândia", "Lins", 
                    "Guaiçara", "Promissão", "Penápolis", "Coroados", "Birigui", 
                    "Araçatuba", "Presidente Prudente", "Martinópolis", "Regente Feijó", "Rancharia", 
                    "Alvares Machado", "Pirapozinho", "Indiana", "Lençóis Paulista", "São Manuel", 
                    "Areiópolis", "Pratânia", "Botucatu", "Bofete", "Pardinho", 
                    "Itatinga", "Duartina", "Gália", "Jafa", "Garça", 
                    "Vera Cruz", "Marília", "Oriente", "Pompéia", "Quintana", 
                    "Herculândia", "Tupã", "Bastos", "Bariri", "Ibitinga", 
                    "Itápolis", "Catanduva", "São José do Rio Preto", "Mirassol", "Olimpia", 
                    "Tanabi", "Ucho", "Santa Adélia", "Bebedouro", "Barretos", 
                    "Ribeirão Preto", "Sertãozinho", "Serrana", "Jardinópolis", "Pontal", 
                    "Cravinhos", "Franca", "Batatais", "São Carlos", "Porto Ferreira", 
                    "Descalvado", "São João da Boa Vista", "Aguai", "São José do Rio Pardo", "Mococa", 
                    "Analandia", "Dourado", "Vargem Grande do Sul", "São Sebastião da Grama", "Casa Branca", 
                    "Santa Cruz das Palmeiras", "Jales", "Fernandópolis", "Votuporanga", "Auriflama", 
                    "Aguas de Santa Barbara", "Arandu", "Avaré", "Cerqueira Cesar", "Iaras", 
                    "Manduri", "Óleo", "Piraju", "Itai", "Aguas de São Pedro", 
                    "São Pedro", "Rio Claro", "Araras", "Leme", "Pirassununga", 
                    "Itirapina", "Analandia", "Santa Maria da Serra", "Brotas", "Cabralia Paulista", 
                    "Espirito Santo do Turvo", "Santa Cruz do Rio Pardo", "Ourinhos", "Ipaussu", "Chavantes", 
                    "Bernardino de Campos", "Canitar", "Salto Grande", "Ibirarema", "Palmital", 
                    "Assis", "Ribeirão do Sul", "Candido Mota", "Taruma", "Maracai", 
                    "Cruzalia", "Araraquara", "Matão", "Jaboticabal", "Monte Alto", 
                    "Taquratinga", "Boa Esperança do Sul", "Bocaina", "Jau", "Pederneiras", 
                    "Barra Bonita", "Igaraçu do Tiete", "Macatuba", "Mineiros do Tiete", "Dois Corregos", 
                    "Torrinha"],
            "Acre": ["Rio Branco", "Cruzeiro do Sul", "Sena Madureira"],
            "Alagoas": ["Maceió", "Arapiraca", "Palmeira dos Índios"],
            "Amazonas": ["Manaus", "Parintins", "Itacoatiara"],
            "Bahia": ["Salvador", "Feira de Santana", "Vitória da Conquista"],
            "Ceará": ["Fortaleza", "Caucaia", "Juazeiro do Norte"],
            "Distrito Federal": ["Brasília", "Taguatinga", "Ceilândia"],
            "Goiás": ["Goiânia", "Aparecida de Goiânia", "Anápolis"],
            "Maranhão": ["São Luís", "Imperatriz", "Caxias"],
            "Mato Grosso": ["Cuiabá", "Várzea Grande", "Rondonópolis"],
            "Mato Grosso do Sul": ["Campo Grande", "Dourados", "Três Lagoas"],
            "Pará": ["Belém", "Ananindeua", "Santarém"],
            "Paraíba": ["João Pessoa", "Campina Grande", "Patos"],
            "Paraná": ["Curitiba", "Londrina", "Maringá"],
            "Pernambuco": ["Recife", "Jaboatão dos Guararapes", "Olinda"],
            "Piauí": ["Teresina", "Parnaíba", "Picos"],
            "Rio Grande do Norte": ["Natal", "Mossoró", "Parnamirim"],
            "Rio Grande do Sul": ["Porto Alegre", "Caxias do Sul", "Pelotas"],
            "Rondônia": ["Porto Velho", "Ji-Paraná", "Ariquemes"],
            "Roraima": ["Boa Vista", "Caracaraí", "Mucajaí"],
            "Santa Catarina": ["Florianópolis", "Joinville", "Blumenau"],
            "Sergipe": ["Aracaju", "Itabaiana", "Lagarto"],
            "Tocantins": ["Palmas", "Araguaína", "Gurupi"]
}

# Rotas para cidades
rotas = {           "Belo Horizonte": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Contagem": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Ibirité": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Sarzedo": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Brumadinho": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Mário Campos": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Divinópolis": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Mateus Leme": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Itaúna": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Juatuba": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Florestal": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Pará de Minas": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Nova Serrana": {"dias_uteis": 1, "dias_entrega": ["Segunda", "Terça"]},
                    "Ribeirão das Neves": {"dias_uteis": 1, "dias_entrega": ["Terça", "Sexta"]},
                    "Veneza": {"dias_uteis": 1, "dias_entrega": ["Terça", "Sexta"]},
                    "Centro": {"dias_uteis": 1, "dias_entrega": ["Terça", "Sexta"]},
                    "Retiro": {"dias_uteis": 1, "dias_entrega": ["Terça", "Sexta"]},
                    "Icaivera": {"dias_uteis": 1, "dias_entrega": ["Terça", "Sexta"]},
                    "Nova Contagem": {"dias_uteis": 1, "dias_entrega": ["Terça", "Sexta"]},
                    "Esmeraldas": {"dias_uteis": 1, "dias_entrega": ["Terça", "Sexta"]},
                    "Betim": {"dias_uteis": 1, "dias_entrega": ["Terça", "Quinta"]},
                    "São Joaquim de Bicas": {"dias_uteis": 1, "dias_entrega": ["Terça", "Quinta"]},
                    "Igarapé": {"dias_uteis": 1, "dias_entrega": ["Terça", "Quinta"]},
                    "Congonhas": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Ouro Branco": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Conselheiro Lafaiete": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Moeda": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Ouro Preto": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Itabirito": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Mariana": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Lagoa Santa": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Vespasiano": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Confins": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "São José da Lapa": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Serro": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Santana do Riacho": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Conceição do Mato Dentro": {"dias_uteis": 1, "dias_entrega": ["Quarta"]},
                    "Pedro Leopoldo": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Matozinhos": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Capim Branco": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Prudente de Morais": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Santa Luzia": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Jaboticatubas": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Nova Lima": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Raposos": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Jardim Canadá": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Barão de Cocais": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Itabira": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Coronel Fabriciano": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "João Monlevade": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Santa Bárbara": {"dias_uteis": 1, "dias_entrega": ["Quinta"]},
                    "Sete Lagoas": {"dias_uteis": 1, "dias_entrega": ["Sexta"]},
                    "Paraopeba": {"dias_uteis": 1, "dias_entrega": ["Sexta"]},
                    "Caetanópolis": {"dias_uteis": 1, "dias_entrega": ["Sexta"]},
                    "Cachoeira da Prata": {"dias_uteis": 1, "dias_entrega": ["Sexta"]},
                    "Inhaúma": {"dias_uteis": 1, "dias_entrega": ["Sexta"]},
                    "Sabará": {"dias_uteis": 1, "dias_entrega": ["Sexta"]},
                    "Caeté": {"dias_uteis": 1, "dias_entrega": ["Sexta"]},
                    "Bom Despacho": {"dias_uteis": 1, "dias_entrega": ["Terça", "Quinta"]},
                    "Montes Claros": {"dias_uteis": 1, "dias_entrega": ["Quarta", "Sexta"]},
                    "Americana": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quinta"]},
                    "Campinas": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quinta"]},
                    "Capivari": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quinta"]},
                    "Hortolândia": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quinta"]},
                    "Itatiba": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quinta"]},
                    "Jundiaí": {"dias_uteis": 4, "dias_entrega":["Segunda", "Quinta"]},
                    "Limeira": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quinta"]},
                    "Piracicaba": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quinta"]},
                    "Mogi das Cruzes": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Caçapava": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Guaratingueta": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Guararema": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Santa Isabel": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "São José dos Campos": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Taubaté": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Lorena": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Cruzeiro": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Norte": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Sul": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Leste": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Oeste": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Osasco": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Guarulhos": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "ABCD": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Santo Andre": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "São Bernardo": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "São Caetano": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Diadema": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Barueri": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Santos": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Praia Grande": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Cubatão": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Itanhaem": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Peruibe": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Mongagua": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "São Vicente": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Bertioga": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Guarujá": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "São Sebastião": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Ubatuba": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Caraguatatuba": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Ilha-Bela": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Itu": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Indaiatuba": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Mairinque": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Salto": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "São Roque": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Sorocaba": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Campos dos Jordão": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "São Bento do Sapucai": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Atibaia": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Bragança Paulista": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Águas de Lindoia": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Socorro": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Jaguariuna": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Holambra": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "São Lourenço da Serra": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Juquitiba": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Miracatu": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Juquia": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Registro": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Pariquera-açu": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Iguape": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Ilha Comprida": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Rio de Janeiro": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Niteroi": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "São Gonçalo": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Duque de Caxias": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Nilópolis": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Mesquita": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Nova Iguaçu": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "SJ de Meriti": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Belford Roxo": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Itaboraí (Centro)": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Magé": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Queimados": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Japeri": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Itaguaí (Centro)": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Seropédica": {"dias_uteis": 2, "dias_entrega": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]},
                    "Barra do Pirai": {"dias_uteis": 2, "dias_entrega": ["Terça"]},
                    "Vassouras": {"dias_uteis": 2, "dias_entrega": ["Terça"]},
                    "Valença": {"dias_uteis": 2, "dias_entrega": ["Terça"]},
                    "Miguel Pereira": {"dias_uteis": 2, "dias_entrega": ["Terça"]},
                    "Paty do Alferes": {"dias_uteis": 2, "dias_entrega": ["Terça"]},
                    "Eng. Paulo de Frontin": {"dias_uteis": 2, "dias_entrega": ["Terça"]},
                    "Mendes": {"dias_uteis": 2, "dias_entrega": ["Terça"]},
                    "Paracambi": {"dias_uteis": 2, "dias_entrega": ["Terça"]},
                    "Pirai": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Pinheral": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Volta Redonda": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Barra Mansa": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Porto Real": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Quatis": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Resende": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Itatiaia": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Mangaratiba": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Angra dos Reis": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Itaguai (além do centro)": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Paraty": {"dias_uteis": 2, "dias_entrega": ["Quarta"]},
                    "Tres Rios": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Petropolis": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Teresópolis": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Nova Friburgo (Lumiar, S.P. da Serra quinzenal)": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Guapimirim": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Cachoeiras de Macacu": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Sumidouro": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Duas Barras": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Bom Jardim": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Cordeiro": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Macuco": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Cantagalo": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Trajano de Morais": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Carmo": {"dias_uteis": 2, "dias_entrega": ["Sexta"]},
                    "Marica": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Saquarema": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Araruama": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Iguaba": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "S.P. da Aldeia": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Cabo Frio": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Buzios": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Arraial do Cabo": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Rio das Ostras": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Macaé": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Silva Jardim": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Casimiro de Abreu": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Itaborai (além do centro)": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Tangua": {"dias_uteis": 2, "dias_entrega": ["Quinta"]},
                    "Bauru": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Agudos": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Piratininga": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Arealva": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Iacanga": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Terça"]},
                    "Araçatuba": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Avai": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Pirajuí": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Guaranta": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Cafelandia": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Lins": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Guaiçara": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Promissão": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Penapolis": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Coroados": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Birigui": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Presidente Prudente": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Martinopolis": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Regente Feijo": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Rancharia": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Alvares Machado": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Pirapozinho": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Indiana": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Lençois Paulista": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "São Manuel": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Areiópolis": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Pratania": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Botucatu": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Bofete": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Pardinho": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Itatinga": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Duartina": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Galia": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Jafa": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Garça": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Vera Cruz": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Marilia": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Oriente": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Pompéia": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Quintana": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Herculandia": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Tupã": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "Bastos": {"dias_uteis": 4, "dias_entrega": ["Segunda", "Quarta"]},
                    "São José do Rio Preto": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Bariri": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Ibitinga": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Itapolis": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Catanduva": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Mirassol": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Olimpia": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Tanabi": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Ucho": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Santa Adelia": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},                   
                    "Barretos": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},
                    "Bebedeuro": {"dias_uteis": 4, "dias_entrega": ["Quinta"]},                    
                    "Ribeirão Preto": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Sertãozinho": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Serrana": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Jardinopolis": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Pontal": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Cravinhos": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},                   
                    "Franca": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},
                    "Batatais": {"dias_uteis": 4, "dias_entrega": ["Sexta"]},                   
                    "Mococa": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "São Carlos": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Porto Ferreira": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Descalvado": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "São Joao da Boa Vista": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Aguai": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "São Jose do Rio Pardo": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Analandia": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Dourado": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Vargem Grande do Sul": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "São Sebastião da Grama": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Casa Branca": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Santa Cruz das Palmeiras": {"dias_uteis": 4, "dias_entrega": ["Terça"]},
                    "Fernandopolis": {"dias_uteis": 4, "dias_entrega": ["Quarta"]},
                    "Jales": {"dias_uteis": 4, "dias_entrega": ["Quarta"]}
                }


# Funções de cálculo
def adicionar_dias_uteis(data, dias_uteis):
    dias_adicionados = 0
    while dias_adicionados < dias_uteis:
        data += timedelta(days=1)
        if data.weekday() < 5:  # Segunda a Sexta
            dias_adicionados += 1
    return data

def proximo_dia_entrega(data_inicial, dias_entrega):
    dias_entrega_indices = [("Segunda", 0), ("Terça", 1), ("Quarta", 2), ("Quinta", 3), ("Sexta", 4)]
    dias_entrega_indices = [index for dia, index in dias_entrega_indices if dia in dias_entrega]

    for i in range(7):
        if data_inicial.weekday() in dias_entrega_indices:
            return data_inicial
        data_inicial += timedelta(days=1)
    return None

def calcular_data_entrega():
    cidade = cidade_var.get()
    data_faturamento_str = cal.get_date()
    data_faturamento = datetime.strptime(data_faturamento_str, "%d/%m/%Y")
    try:
        volume = float(volume_entry.get())
    except ValueError:
        resultado_var.set("Volume inválido.")
        return

    if cidade in rotas:
        if volume > 500:
            resultado_var.set("Volume superior ao esperado. Necessário cotar frete com logística.")
            return
        elif volume < 30:
            resultado_var.set("Volume insuficiente.")
            return
    
    if cidade not in rotas:
        resultado_var.set("Cidade não encontrada na lista de rotas.")
        return

    dias_uteis = rotas[cidade]["dias_uteis"]
    dias_entrega = rotas[cidade]["dias_entrega"]

    data_entrega_inicial = adicionar_dias_uteis(data_faturamento, dias_uteis)
    data_entrega_final = proximo_dia_entrega(data_entrega_inicial, dias_entrega)
    
    if data_entrega_final:
        dias_da_semana = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
        dia_da_semana = dias_da_semana[data_entrega_final.weekday()]
        resultado_var.set(f"Data de entrega para {cidade}: {dia_da_semana}, {data_entrega_final.strftime('%d-%m-%Y')}")
    else:
        resultado_var.set("Não há datas de entrega disponíveis.")

# Funções para gerenciamento de telas
def mostrar_tela_selecao_estado():
    estado = estado_var.get()
    if not estado:
        return  # Não avançar se não tiver um estado selecionado

    # Oculta a tela inicial de seleção de estado
    estado_label.pack_forget()
    voltar_button.pack_forget()
    estado_menu.pack_forget()
    avancar_button.pack_forget()
    

    # Exibe a tela de seleção de cidade
    cidade_label.pack(pady=15)
    cidade_menu.pack(pady=10, padx=30)
    volume_label.pack(pady=5)
    volume_entry.pack(pady=5, padx=30)
    cal.pack(pady=10, padx=10)
    calcular_button.pack(pady=5, padx=30)
    voltar_button.place(relx=0.0, rely=0.0, x=10, y=10, anchor="nw")
    resultado_label.pack(pady=15)
    atualizar_cidades()

def atualizar_cidades(*args):
    estado = estado_var.get()
    cidades = estados.get(estado, [])
    cidade_menu['values'] = cidades
    cidade_var.set(cidades[0] if cidades else "")

def voltar_para_selecao_estado():
    voltar_button.pack_forget()
    cidade_label.pack_forget()
    cidade_menu.pack_forget()
    cal.pack_forget()
    calcular_button.pack_forget()
    resultado_label.pack_forget()
    volume_entry.pack_forget()
    volume_label.pack_forget()
    estado_label.pack(pady=15)
    estado_menu.pack(pady=10, padx=30)
    avancar_button.pack(pady=15)

# Função para abrir a tela "Como funciona?"
def abrir_tela_como_funciona():
    como_funciona_window = tk.Toplevel(tela_principal)
    como_funciona_window.title("Como Funciona o Cálculo de Rotas")
    como_funciona_window.geometry("400x400")
    como_funciona_window.configure(bg="#08A2E0")

    explicacao_label = tk.Label(
        como_funciona_window,
        text="A lógica do cálculo de rota considera os seguintes fatores:\n\n"
             "1. Cidade de destino e suas respectivas datas de rotas.\n"
             "2. Data de faturamento (após 15h, a entrega é adiada).\n"
             "3. Prazo mínimo de transferência (Ex. 4 dias utéis para SP, 2 Dias úteis para RJ.).\n\n"
             "A rota é calculada automaticamente com base nesses critérios, "       
             "otimizando o tempo de entrega para cada localidade.",
        font=("Arial", 12),
        foreground="black",
        background="#08A2E0",
        wraplength=350,
        justify="left"
    )
    explicacao_label.pack(pady=20, padx=10)

# Interface gráfica principal
tela_principal = tk.Tk()
tela_principal.title("Frota Fruta")
tela_principal.geometry("540x760")
tela_principal.configure(bg="#08A2E0")


font_style = ("Irresistible", 15)
estado_var = tk.StringVar()
cidade_var = tk.StringVar()
volume_var = tk.StringVar()
resultado_var = tk.StringVar()

# Configuração de estilo
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#007BFF", foreground="black", font=("Arial", 12))

# Carregar imagens e ícones
logo_path = "C:\\Users\\Vendas\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\Logo.png"
logo_image = Image.open(logo_path).resize((400, 210), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

icon_path = "C:\\Users\\Vendas\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\icon.ico"
icon_image = Image.open(icon_path).resize((128, 128), Image.LANCZOS)
icon_photo = ImageTk.PhotoImage(icon_image)
tela_principal.iconphoto(True, icon_photo)

# Componentes da interface
logo_label = tk.Label(tela_principal, image=logo_photo, bg="#08A2E0")
logo_label.pack(side="top")

estado_label = ttk.Label(tela_principal, text="Selecione o Estado:", font=font_style, foreground="white", background="#08A2E0")
estado_label.pack(pady=15)

estado_menu = autocombobox.AutoCombobox(tela_principal, textvariable=estado_var, values=list(estados.keys()), font=font_style)
estado_menu.pack(pady=10, padx=30)

avancar_button = ttk.Button(tela_principal, text="Avançar", command=mostrar_tela_selecao_estado, width=10, padding=10)
avancar_button.pack(pady=10)

cidade_label = ttk.Label(tela_principal, text="Cidade:", font=font_style, foreground="#ffffff", background="#08A2E0")
cidade_menu = autocombobox.AutoCombobox(tela_principal, textvariable=cidade_var, font=font_style)

volume_label = ttk.Label(tela_principal, text="Volume (kg):", font=font_style, background="#08A2E0", foreground="#ffffff")
volume_entry = ttk.Entry(tela_principal, textvariable=volume_var, font=font_style)

cal = Calendar(tela_principal, selectmode="day", date_pattern="dd/mm/yyyy", background="#0008E0", foreground="white", font=font_style)

calcular_button = ttk.Button(tela_principal, text="CALCULAR", command=calcular_data_entrega, width=15, padding=1)

resultado_label = ttk.Label(tela_principal, textvariable=resultado_var, font=("IMPACT", 17), foreground="green", background="#F5FFFA", borderwidth=20, relief="solid")

como_funciona_button = ttk.Button(tela_principal, text="?", style='info.TButton', command=abrir_tela_como_funciona, width=5)
como_funciona_button.place(relx=1.0, rely=0.0, x=-10, y=10, anchor="ne")

voltar_button = ttk.Button(tela_principal, text="Voltar", command=voltar_para_selecao_estado, width=5, padding=5)
voltar_button.place(relx=0.0, rely=0.0, x=10, y=10, anchor="nw")

rodape_label = ttk.Label(tela_principal, text="BY: Daniel Felipe Versão Alpha 2.0.1", font=("Arial", 7), foreground="white", background="#2a2d2e")
rodape_label.pack(side="bottom")

# Inicia a interface
tela_principal.mainloop()     