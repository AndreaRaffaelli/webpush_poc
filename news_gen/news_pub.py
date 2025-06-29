#!/usr/bin/env python3
"""
Script CLI per generare notizie in stile anni 2000-2010 da un database locale
Non richiede API key - usa notizie pre-scritte nostalgiche
"""

import argparse
import json
import random
import requests
import sys
from datetime import datetime
from typing import Dict, List

# Configurazione
SERVER_URL = "http://localhost:5000/publish"  # Modifica con l'URL del tuo server

class NewsGenerator:
    def __init__(self, server_url: str = None):
        self.server_url = server_url or SERVER_URL
        # Database di notizie in stile anni 2000-2010
        self.news_database = {
            "tech": [
                {
                    "title": "INCREDIBILE! Nuovo iPod Video da 60GB può contenere 15.000 canzoni!",
                    "body": "Apple ha appena lanciato il rivoluzionario iPod Video! Con ben 60GB di memoria, potrai portare con te tutta la tua collezione musicale. E ora puoi anche guardare episodi di Lost e Desperate Housewives! Il futuro è qui, ragazzi!"
                },
                {
                    "title": "YouTube: il sito dove TUTTI possono diventare famosi!",
                    "body": "Hai mai sognato di essere in TV? Con YouTube ora è possibile! Basta una webcam e puoi caricare i tuoi video. Alcuni utenti stanno già diventando delle vere celebrità di Internet. Che epoca fantastica per essere vivi!"
                },
                {
                    "title": "Nokia N95: il telefono che fa TUTTO! Fotocamera, GPS e Internet!",
                    "body": "Il nuovo Nokia N95 è praticamente un computer in tasca! Ha una fotocamera da 5 megapixel, GPS integrato e puoi navigare su Internet. Chi ha bisogno di un laptop quando hai questo gioiello tecnologico?"
                },
                {
                    "title": "MySpace supera Google come sito più visitato al mondo!",
                    "body": "MySpace è ufficialmente il re di Internet! Tutti stanno personalizzando i loro profili con musica, glitter e HTML colorato. È il posto dove scoprire nuove band e fare amicizie. Tom è davvero il nostro migliore amico!"
                },
                {
                    "title": "BlackBerry: l'email sempre in tasca! I manager impazziscono di gioia!",
                    "body": "Con il BlackBerry puoi ricevere email istantaneamente ovunque ti trovi! È come avere l'ufficio sempre con te. La tastiera QWERTY è perfetta per scrivere velocemente. Il lavoro non sarà mai più lo stesso!"
                }
            ],
            "entertainment": [
                {
                    "title": "Grande Fratello 6: Maria Monsè fa scandalo con le sue dichiarazioni!",
                    "body": "La casa più spiata d'Italia è in subbuglio! Maria Monsè ha fatto delle rivelazioni shock che stanno facendo impazzire il pubblico. Domani sera puntata imperdibile su Canale 5! Chi sarà eliminato?"
                },
                {
                    "title": "ESCLUSIVO: Britney Spears e Justin Timberlake si sono lasciati!",
                    "body": "La coppia più bella di Hollywood si è detta addio! Britney e Justin hanno annunciato la fine della loro relazione. I fan sono devastati. Cosa succederà ora alla principessa del pop?"
                },
                {
                    "title": "Lost: cosa significa davvero la serie? I fan impazziscono per le teorie!",
                    "body": "L'isola misteriosa di Lost continua a tenere incollati milioni di spettatori. Sui forum di Internet si moltiplicano le teorie: viaggi nel tempo? Esperimenti scientifici? Una cosa è certa: mercoledì sera tutti davanti alla TV!"
                },
                {
                    "title": "American Idol: Kelly Clarkson conquista l'America con la sua voce!",
                    "body": "La prima vincitrice di American Idol ha dimostrato che i sogni possono diventare realtà! Kelly Clarkson sta scalando tutte le classifiche musicali. Il talent show di Fox sta rivoluzionando il mondo della musica!"
                },
                {
                    "title": "Matrix Reloaded: effetti speciali che lasciano senza fiato!",
                    "body": "I fratelli Wachowski hanno superato se stessi! Le scene d'azione di Matrix Reloaded sono spettacolari. Neo è più forte che mai e la realtà virtuale non è mai stata così realistica. Il cinema non sarà mai più lo stesso!"
                }
            ],
            "lifestyle": [
                {
                    "title": "Tamagotchi: il nuovo fenomeno che sta conquistando tutti!",
                    "body": "L'animaletto virtuale che vive nel tuo portachiavi è diventato un must-have! Devi nutrirlo, coccolarlo e giocare con lui. Attenzione: se non te ne prendi cura... muore! È una responsabilità seria, ma che divertimento!"
                },
                {
                    "title": "MSN Messenger: chattare non è mai stato così cool!",
                    "body": "Con MSN Messenger puoi parlare con tutti i tuoi amici contemporaneamente! Le emoticon animate sono fantastiche e puoi personalizzare il tuo nickname con caratteri speciali. La comunicazione del futuro è qui!"
                },
                {
                    "title": "DVD: addio videocassette! La qualità video è cristallina!",
                    "body": "I DVD stanno rivoluzionando il modo di guardare film! Niente più riavvolgere, qualità perfetta e contenuti extra incredibili. Blockbuster sta già riempiendo gli scaffali. È l'era del digitale!"
                },
                {
                    "title": "Second Life: crea la tua vita virtuale perfetta!",
                    "body": "Nel mondo virtuale di Second Life puoi essere chiunque vuoi! Compra terreni virtuali, incontra persone da tutto il mondo e vivi una seconda vita online. Alcune aziende stanno aprendo negozi virtuali. Il futuro è arrivato!"
                },
                {
                    "title": "Ringtones personalizzate: il tuo cellulare non sarà più anonimo!",
                    "body": "Basta con la solita suoneria! Ora puoi scaricare la tua canzone preferita come ringtone. Da 50 Cent a Evanescence, scegli il suono che ti rappresenta. Il tuo Nokia suonerà come nessun altro!"
                }
            ],
            "social": [
                {
                    "title": "Wikipedia: l'enciclopedia che scrive il popolo!",
                    "body": "Addio Encarta! Wikipedia è l'enciclopedia libera dove tutti possono contribuire. Informazioni su qualsiasi argomento, scritte da persone comuni. È la democratizzazione della conoscenza! Incredibile cosa può fare Internet!"
                },
                {
                    "title": "Blog: tutti possono diventare giornalisti!",
                    "body": "Con Blogger e LiveJournal chiunque può aprire il proprio diario online! Condividi pensieri, foto e esperienze con il mondo intero. I blog stanno cambiando il modo di comunicare. Benvenuti nella blogosfera!"
                },
                {
                    "title": "Fotocamere digitali: addio rullini! Le foto si vedono subito!",
                    "body": "Le fotocamere digitali sono il futuro della fotografia! Scatta centinaia di foto senza sprecare pellicola e vedi subito il risultato. Con la scheda di memoria puoi salvare ricordi infiniti. Che rivoluzione!"
                },
                {
                    "title": "PlayStation 2: la console più venduta di sempre!",
                    "body": "PS2 ha conquistato il mondo! Con giochi come Grand Theft Auto e Final Fantasy, Sony ha creato la console perfetta. E ora puoi anche guardare DVD! Il sogno di ogni gamer è diventato realtà."
                },
                {
                    "title": "LimeWire: condividi musica con tutto il mondo!",
                    "body": "Con LimeWire puoi scaricare qualsiasi canzone gratuitamente! La condivisione peer-to-peer sta rivoluzionando la distribuzione musicale. Attenzione ai virus, ma che libertà! La musica è finalmente di tutti!"
                }
            ]
        }
        
        # Frasi di apertura tipiche dell'epoca
        self.opening_phrases = [
            "BOMBA! ",
            "INCREDIBILE! ",
            "ESCLUSIVO! ",
            "SHOCK! ",
            "RIVOLUZIONE! ",
            "FENOMENO! ",
            "BREAKING NEWS! ",
            "HOT! "
        ]
        
        # Emoji e simboli dell'epoca
        self.retro_symbols = ["★", "♪", "♫", "☆", "♥", "→", "←", "↑", "↓"]

    def get_random_news(self, category: str = None) -> Dict:
        """Ottiene una notizia casuale dal database"""
        if category and category in self.news_database:
            news_list = self.news_database[category]
        else:
            # Scegli categoria casuale
            all_categories = list(self.news_database.keys())
            category = random.choice(all_categories)
            news_list = self.news_database[category]
        
        news = random.choice(news_list)
        
        # Aggiungi qualche tocco random dell'epoca
        title = news["title"]
        if random.random() < 0.3:  # 30% possibilità di aggiungere frase di apertura
            opener = random.choice(self.opening_phrases)
            if not title.startswith(tuple(self.opening_phrases)):
                title = opener + title
        
        return {
            "title": title,
            "body": news["body"],
            "category": category
        }

    def list_categories(self):
        """Mostra tutte le categorie disponibili"""
        print("📋 Categorie disponibili:")
        for category, news_list in self.news_database.items():
            print(f"  • {category}: {len(news_list)} notizie")
        
        print(f"\n📊 Totale notizie: {sum(len(news) for news in self.news_database.values())}")

    def list_all_news(self):
        """Mostra tutte le notizie disponibili"""
        for category, news_list in self.news_database.items():
            print(f"\n📁 {category.upper()}:")
            for i, news in enumerate(news_list, 1):
                print(f"  {i:2d}. {news['title']}")

    def send_notification(self, title: str, body: str) -> Dict:
        """Invia la notifica al server"""
        payload = {
            "title": title,
            "body": body
        }
        
        try:
            response = requests.post(
                self.server_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Errore invio notifica: {e}")

    def generate_and_send(self, category: str = None, dry_run: bool = False) -> Dict:
        """Genera una notizia casuale e la invia"""
        print("🎲 Selezione notizia casuale...")
        
        # Ottieni notizia casuale
        news = self.get_random_news(category)
        
        print(f"✅ Notizia selezionata dalla categoria '{news['category']}':")
        print(f"📰 TITOLO: {news['title']}")
        print(f"📄 CORPO: {news['body']}\n")
        
        if dry_run:
            print("🔍 Modalità preview - nessuna notifica inviata")
            return {"status": "preview", "title": news['title'], "body": news['body']}
        
        # Invia notifica
        print("📱 Invio notifica push...")
        result = self.send_notification(news['title'], news['body'])
        
        if result.get("status") == "sent":
            print(f"✅ Notifica inviata con successo a {result.get('success', 0)} dispositivi!")
        elif result.get("status") == "partial":
            print(f"⚠️  Notifica parzialmente inviata: {result.get('success', 0)} successi, {result.get('failure', 0)} fallimenti")
        else:
            print("❌ Errore nell'invio della notifica")
            
        return result

def main():
    parser = argparse.ArgumentParser(
        description="Generatore di notizie nostalgiche anni 2000-2010",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  python news_generator.py                          # Notizia casuale
  python news_generator.py --category tech         # Solo notizie tech
  python news_generator.py --preview               # Solo preview
  python news_generator.py --list-categories       # Mostra categorie
  python news_generator.py --list-all              # Mostra tutte le notizie
        """
    )
    
    parser.add_argument(
        "--category",
        choices=["tech", "entertainment", "lifestyle", "social"],
        help="Categoria specifica (tech, entertainment, lifestyle, social)"
    )
    
    parser.add_argument(
        "--preview", 
        action="store_true",
        help="Modalità preview: mostra la notizia senza inviarla"
    )
    
    parser.add_argument(
        "--list-categories", 
        action="store_true",
        help="Mostra tutte le categorie disponibili"
    )
    
    parser.add_argument(
        "--list-all", 
        action="store_true",
        help="Mostra tutte le notizie del database"
    )
    
    parser.add_argument(
        "--server-url",
        default=SERVER_URL,
        help=f"URL del server di notifiche (default: {SERVER_URL})"
    )
    
    args = parser.parse_args()

    generator = NewsGenerator(args.server_url)
    
    if args.list_categories:
        generator.list_categories()
        return
    
    if args.list_all:
        generator.list_all_news()
        return
    
    try:
        # Genera e invia notizia
        print("🚀 News Generator 2000s - Nostalgia Mode Activated!")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Aggiungi un po' di ASCII art nostalgico
        symbols = random.sample(generator.retro_symbols, 3)
        print(f"✨ {symbols[0]} WELCOME TO THE GOLDEN AGE OF INTERNET {symbols[1]} ✨\n")
        
        result = generator.generate_and_send(
            category=args.category,
            dry_run=args.preview
        )
        
        print(f"\n📊 Risultato: {result}")
        print(f"🎯 Nostalgia level: OVER 9000! {random.choice(generator.retro_symbols)}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Operazione interrotta dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
