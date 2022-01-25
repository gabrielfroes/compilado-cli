import os, sys
import argparse
import configparser
from photoshopy import Photoshopy
from compilado_feed import CompiladoFeed
from compilado_formatter import CompiladoFormatter
import logging

class CompiladoCLI:
    CLI_VERSION = "Compilado CLI 1.0.0"
    INI_FILE = "compilado.ini"

    def __load_ini_file(self, filename):
        full_path = os.path.abspath(os.path.join("./src", filename))
        path_config_file = full_path if os.path.isfile(full_path) else \
            os.path.abspath(os.path.join(os.path.dirname(sys.executable), filename))
        self.config = configparser.ConfigParser()
        if self.config.read(path_config_file):
            return True
        else:
            logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='compilado.log')
            logging.error("Não foi possível carregar o arquivo de configuração em {}".format(path_config_file))
            return False

    def __init__(self):
        if self.__load_ini_file(self.INI_FILE):
            self.__run()

    def __run(self):
        self.parser = argparse.ArgumentParser(
            prog="compilado",
            description="Automação para o Compilado (Newsletter e Podcast)",
            epilog="Desenvolvido por: Código Fonte TV",
            usage="%(prog)s [options]")

        self.parser.version = self.CLI_VERSION
        self.parser.add_argument("-v", "--version", action="version")

        subparsers = self.parser.add_subparsers(help="Ações Compilado")

        self.__create_thumbnail_parser(subparsers)

        parser_args = self.parser.parse_args()
        if parser_args:
            try:
                if parser_args.auto:
                    self.__auto_generate_thumbnail(parser_args.dest)
                elif parser_args.episodio and parser_args.periodo:
                    self.__generate_thumbnail(parser_args.episodio, parser_args.periodo, parser_args.dest)
            except Exception as e:
                print("Argumento inválido: {}".format(e))
                sys.exit(1)
        else:
            self.parser.print_help()
            sys.exit(1)
    
    def __create_thumbnail_parser(self, subparsers):
        self.thumbnail_parser = subparsers.add_parser("thumbnail", help="Gerador de thumbnails")
        self.thumbnail_parser.add_argument("--auto", "-a", help="Gerador de thumbnail a partir de RSS", action="store_true", required=False)
        self.thumbnail_parser.add_argument("--episodio", "-e", help="Número do episódio", type=str, required=False)
        self.thumbnail_parser.add_argument("--periodo", "-p", help="Período - ex: \"01/01 a 06/01\"", type=str, required=False)
        self.thumbnail_parser.add_argument("--dest", "-d", help="Pasta de destino (opcional)", type=str, default=".")

    def __check_psd_file(self, file_name):
        if file_name.endswith(".psd"):
            return True
        else:
            return False

    def __auto_generate_thumbnail(self, destination):
        feed_url = self.config["feed"]["url"]
        feed = CompiladoFeed(feed_url)
        episode = feed.next_episode()
        if episode:
            formatter = CompiladoFormatter()
            episode_id = formatter.episode(episode["id"])
            episode_period = formatter.period(episode["period"]["start"], episode["period"]["end"])
            self.__generate_thumbnail(episode_id, episode_period, destination)

    def __generate_thumbnail(self, episode, period, destination):
        psds_origin = self.config["path"]["psds_origin"]
        files = self.config["files"]["psds"].split("|")
        destination = os.path.abspath(os.path.join(destination))

        psds = filter(self.__check_psd_file, [os.path.join(psds_origin, file) for file in files])
        if psds:
            app = Photoshopy()
            for psd in psds:
                psd_name = os.path.basename(psd)
                jpg_name = psd_name.replace(".psd", ".jpg")
                if app.openPSD(psd):
                    app.updateLayerText("NUMERO_EPISODIO", episode)
                    app.updateLayerText("PERIODO", period)
                    app.exportJPEG(jpg_name, destination)
                    print("Exportando... {}".format(jpg_name))
                    app.closePSD()
            app.closePhotoshop()
        else:
            print("Nenhum arquivo PSD encontrado")