import json
import os
import csv
from typing import List, Dict, Optional

DATA_FILE = "data_store.json"
BOX_CAPACITY = 10

class Part:
    def __init__(self, pid: int, weight: float, color: str, length: float):
        self.id = pid
        self.weight = weight
        self.color = color
        self.length = length
        self.approved = False
        self.rejection_reasons: List[str] = []

    def evaluate(self):
        self.rejection_reasons = []
        # Criteria from project spec
        if not (95 <= self.weight <= 105):
            self.rejection_reasons.append(f"Peso fora do intervalo (95-105g): {self.weight}g")
        if self.color.lower() not in ("azul", "verde"):
            self.rejection_reasons.append(f"Cor inválida (esperado 'azul' ou 'verde'): {self.color}")
        if not (10 <= self.length <= 20):
            self.rejection_reasons.append(f"Comprimento fora do intervalo (10-20cm): {self.length}cm")
        self.approved = len(self.rejection_reasons) == 0
        return self.approved

    def to_dict(self):
        return {
            "id": self.id,
            "weight": self.weight,
            "color": self.color,
            "length": self.length,
            "approved": self.approved,
            "rejection_reasons": self.rejection_reasons
        }

    @staticmethod
    def from_dict(d):
        p = Part(d["id"], d["weight"], d["color"], d["length"])
        p.approved = d.get("approved", False)
        p.rejection_reasons = d.get("rejection_reasons", [])
        return p

class Box:
    def __init__(self, box_id: int):
        self.id = box_id
        self.part_ids: List[int] = []
        self.closed: bool = False

    def add_part(self, pid: int):
        if self.closed:
            raise ValueError("Caixa já está fechada.")
        self.part_ids.append(pid)
        if len(self.part_ids) >= BOX_CAPACITY:
            self.closed = True

    def remove_part(self, pid: int):
        if pid in self.part_ids:
            self.part_ids.remove(pid)
        # Nota: não reabrimos caixas fechadas automaticamente

    def to_dict(self):
        return {"id": self.id, "part_ids": self.part_ids, "closed": self.closed}

    @staticmethod
    def from_dict(d):
        b = Box(d["id"])
        b.part_ids = d.get("part_ids", [])
        b.closed = d.get("closed", False)
        return b

class Warehouse:
    def __init__(self):
        self.next_id = 1
        self.parts: Dict[int, Part] = {}
        self.boxes: List[Box] = []

    def load(self, filename=DATA_FILE):
        if not os.path.exists(filename):
            return
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.next_id = data.get("next_id", 1)
        self.parts = {int(k): Part.from_dict(v) for k, v in data.get("parts", {}).items()}
        self.boxes = [Box.from_dict(b) for b in data.get("boxes", [])]

    def save(self, filename=DATA_FILE):
        data = {
            "next_id": self.next_id,
            "parts": {str(k): v.to_dict() for k, v in self.parts.items()},
            "boxes": [b.to_dict() for b in self.boxes]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def create_part(self, weight: float, color: str, length: float) -> Part:
        p = Part(self.next_id, weight, color, length)
        p.evaluate()
        self.parts[p.id] = p
        self.next_id += 1
        if p.approved:
            self._store_in_box(p.id)
        return p

    def _store_in_box(self, part_id: int):
        box = self._get_open_box()
        if box is None:
            box = Box(len(self.boxes) + 1)
            self.boxes.append(box)
        box.add_part(part_id)

    def _get_open_box(self) -> Optional[Box]:
        for b in reversed(self.boxes):
            if not b.closed:
                return b
        return None

    def remove_part(self, part_id: int) -> bool:
        if part_id not in self.parts:
            return False
        # remove from boxes if present
        for b in self.boxes:
            if part_id in b.part_ids:
                b.remove_part(part_id)
                # do not reopen closed boxes
        del self.parts[part_id]
        return True

    def list_parts(self, approved: Optional[bool]=None) -> List[Part]:
        res = []
        for p in self.parts.values():
            if approved is None or p.approved == approved:
                res.append(p)
        return sorted(res, key=lambda x: x.id)

    def list_boxes(self) -> List[Box]:
        return self.boxes

    def generate_report(self) -> Dict:
        approved = [p for p in self.parts.values() if p.approved]
        rejected = [p for p in self.parts.values() if not p.approved]
        return {
            "total_parts": len(self.parts),
            "approved_count": len(approved),
            "rejected_count": len(rejected),
            "rejected_details": {p.id: p.rejection_reasons for p in rejected},
            "boxes": [b.to_dict() for b in self.boxes]
        }

    def export_report_csv(self, filename="relatorio_final.csv"):
        report = self.generate_report()
        with open(filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Tipo", "ID", "Detalhe"])
            writer.writerow(["Total de pecas", report["total_parts"], ""])
            writer.writerow(["Aprovadas", report["approved_count"], ""])
            writer.writerow(["Reprovadas", report["rejected_count"], ""])
            writer.writerow([])
            writer.writerow(["Reprovacoes"])
            writer.writerow(["ID", "Motivos"])
            for pid, motivos in report["rejected_details"].items():
                writer.writerow([pid, "; ".join(motivos)])
            writer.writerow([])
            writer.writerow(["Caixas"])
            writer.writerow(["Caixa ID", "Fechada", "Quantidade de pecas", "IDs"])
            for b in report["boxes"]:
                writer.writerow([b["id"], b["closed"], len(b["part_ids"]), ",".join(map(str, b["part_ids"]))])

# CLI / Menu
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("Pressione Enter para continuar...")

def main():
    wh = Warehouse()
    wh.load()

    while True:
        clear_screen()
        print("=== Desafio Automação Digital ===")
        print("1) Cadastrar nova peça")
        print("2) Listar peças aprovadas")
        print("3) Listar peças reprovadas")
        print("4) Remover peça cadastrada")
        print("5) Listar caixas")
        print("6) Gerar relatório final (console + CSV)")
        print("0) Sair")
        escolha = input("Escolha: ").strip()

        if escolha == "1":
            try:
                weight = float(input("Peso (g): ").strip())
                color = input("Cor: ").strip()
                length = float(input("Comprimento (cm): ").strip())
            except ValueError:
                print("Entrada inválida - valores numéricos esperados.")
                pause()
                continue
            part = wh.create_part(weight, color, length)
            if part.approved:
                print(f"Peça cadastrada e APROVADA (id={part.id}).")
            else:
                print(f"Peça cadastrada e REPROVADA (id={part.id}). Motivos:")
                for m in part.rejection_reasons:
                    print(" - " + m)
            wh.save()
            pause()

        elif escolha == "2":
            approved = wh.list_parts(approved=True)
            if not approved:
                print("Nenhuma peça aprovada encontrada.")
            else:
                for p in approved:
                    print(f"[ID {p.id}] Peso:{p.weight}g Cor:{p.color} Comp:{p.length}cm")
            pause()

        elif escolha == "3":
            rejected = wh.list_parts(approved=False)
            if not rejected:
                print("Nenhuma peça reprovada encontrada.")
            else:
                for p in rejected:
                    print(f"[ID {p.id}] Peso:{p.weight}g Cor:{p.color} Comp:{p.length}cm")
                    for m in p.rejection_reasons:
                        print("  - " + m)
            pause()

        elif escolha == "4":
            try:
                pid = int(input("Digite o ID da peça a remover: ").strip())
            except ValueError:
                print("ID inválido.")
                pause()
                continue
            ok = wh.remove_part(pid)
            if ok:
                print("Peça removida com sucesso.")
                wh.save()
            else:
                print("Peça não encontrada.")
            pause()

        elif escolha == "5":
            boxes = wh.list_boxes()
            if not boxes:
                print("Nenhuma caixa criada.")
            else:
                for b in boxes:
                    status = "Fechada" if b.closed else "Aberta"
                    print(f"Caixa {b.id} - {status} - {len(b.part_ids)} peças -> IDs: {b.part_ids}")
            pause()

        elif escolha == "6":
            report = wh.generate_report()
            print("RELATÓRIO FINAL")
            print(f"Total de peças cadastradas: {report['total_parts']}")
            print(f"Total aprovadas: {report['approved_count']}")
            print(f"Total reprovadas: {report['rejected_count']}")
            print("Detalhes das reprovações:")
            for pid, motivos in report["rejected_details"].items():
                print(f" ID {pid}:")
                for m in motivos:
                    print("   - " + m)
            print("Caixas:")
            for b in report["boxes"]:
                print(f" Caixa {b['id']} - {'Fechada' if b['closed'] else 'Aberta'} - {len(b['part_ids'])} peças")
            wh.export_report_csv("relatorio_final.csv")
            print("Relatório exportado para 'relatorio_final.csv'.")
            pause()

        elif escolha == "0":
            print("Encerrando. Dados salvos em", DATA_FILE)
            wh.save()
            break
        else:
            print("Opção inválida.")
            pause()

if __name__ == "__main__":
    main()
