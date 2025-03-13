import pandas as pd
from typing import List


class ChunkProcessor:
    def __init__(self, file_path: str):
        """
        Inicializálja a chunk processzort Excel fájlokhoz.

        :param file_path: Az Excel fájl elérési útvonala.
        """
        self.file_path = file_path

    def load_and_process_chunks(self) -> List[str]:
        """
        Betölti az Excelt és összekapcsolja az oszlopokat chunkokká.

        :param file_path: Az Excel fájl elérési útvonala
        :return: Egy listája a teljes chunkoknak (kérdés + válasz)
        """
        df = pd.read_excel(self.file_path, header=None)  # Fejléc nélküli betöltés
        df.dropna(inplace=True)  # Üres sorok eltávolítása

        # Összekapcsoljuk a kérdést és választ egy stringgé
        chunks = df.apply(lambda row: f"Kérdés: {row[0]}\nVálasz: {row[1]}", axis=1).tolist()
        return chunks



