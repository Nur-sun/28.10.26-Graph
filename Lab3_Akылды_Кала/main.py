"""Ақылды қала: ең тиімді маршрутты анықтау жүйесі."""
from pathlib import Path
from graph import CityGraph
from dijkstra import dijkstra
from visualization import draw_graph

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "city_graph.json"

def print_route(result, start, finish, mode):
    print("\n" + "="*54)
    print("НӘТИЖЕ")
    print(f"Режим: {'Қашықтық' if mode == 'distance' else 'Уақыт'}")
    if start == finish:
        print(f"Маршрут: {start} (бастапқы және соңғы төбе бірдей)")
        print("Жалпы салмақ: 0")
    elif result["total"] is None:
        print(f"{start} → {finish}: маршрут табылмады.")
    else:
        print("Ең қысқа маршрут:", " → ".join(result["route"]))
        print(f"Жалпы салмақ: {result['total']:g}")
    print("Қаралған төбелер реті:", " → ".join(result["visited_order"]))
    print("Қаралған төбелер саны:", result["visited_count"])
    print(f"Орындалу уақыты: {result['elapsed_ms']:.4f} мс")
    print("\nБастапқы төбеден барлық қолжетімді төбелерге дейін:")
    for node, distance in result["distances"].items():
        print(f"  {node}: {'∞' if distance == float('inf') else f'{distance:g}'}")
    print("="*54)

def main():
    graph = CityGraph()
    if DATA_FILE.exists():
        try:
            graph.load(DATA_FILE)
        except Exception as exc:
            print("JSON жүктелмеді, бастапқы граф пайдаланылады:", exc)
    else:
        graph.save(DATA_FILE)

    while True:
        print("""
===== АҚЫЛДЫ ҚАЛА | МӘЗІР =====
1. Ең тиімді маршрутты есептеу
2. Графты визуализациялау
3. Қабырға қосу
4. Қабырға жою
5. Қабырға салмағын өзгерту
6. Жолды уақытша жабу/ашу
7. Төбе қосу
8. Төбе жою
9. Графты JSON файлына сақтау
10. JSON файлынан қайта жүктеу
0. Шығу
""")
        choice = input("Таңдаңыз: ").strip()
        try:
            if choice == "0":
                graph.save(DATA_FILE)
                print("Деректер сақталды. Сау болыңыз!")
                break
            elif choice == "1":
                start = input(f"Бастапқы төбе {graph.nodes}: ").strip().upper()
                finish = input("Соңғы төбе: ").strip().upper()
                mode = input("Режим (1-қашықтық, 2-уақыт): ").strip()
                mode = "time" if mode == "2" else "distance"
                result = dijkstra(graph, start, finish, mode)
                print_route(result, start, finish, mode)
                if result["total"] is not None:
                    draw_graph(graph, result, mode)
            elif choice == "2":
                start = input("Маршруттың бастапқы төбесі (өткізуге болады): ").strip().upper()
                finish = input("Маршруттың соңғы төбесі (өткізуге болады): ").strip().upper()
                mode = "time" if input("Режим (1-қашықтық, 2-уақыт): ").strip()=="2" else "distance"
                result = dijkstra(graph,start,finish,mode) if start and finish else None
                draw_graph(graph,result,mode)
            elif choice == "3":
                a=input("Бірінші төбе: ").strip().upper(); b=input("Екінші төбе: ").strip().upper()
                d=float(input("Қашықтық салмағы: ")); t=float(input("Уақыт салмағы: "))
                graph.add_edge(a,b,d,t); print("Қабырға қосылды.")
            elif choice == "4":
                graph.remove_edge(input("Бірінші төбе: ").strip().upper(),input("Екінші төбе: ").strip().upper())
                print("Қабырға жойылды.")
            elif choice == "5":
                a=input("Бірінші төбе: ").strip().upper(); b=input("Екінші төбе: ").strip().upper()
                d=input("Жаңа қашықтық (өзгермесе бос): ").strip()
                t=input("Жаңа уақыт (өзгермесе бос): ").strip()
                graph.set_weight(a,b,float(d) if d else None,float(t) if t else None)
                print("Салмақ жаңартылды.")
            elif choice == "6":
                a=input("Бірінші төбе: ").strip().upper(); b=input("Екінші төбе: ").strip().upper()
                close=input("Жабу үшін 1, қайта ашу үшін 0: ").strip()=="1"
                graph.toggle_edge(a,b,close); print("Жол күйі жаңартылды.")
            elif choice == "7":
                graph.add_node(input("Жаңа төбе атауы: ")); print("Төбе қосылды.")
            elif choice == "8":
                graph.remove_node(input("Жойылатын төбе: ").strip().upper()); print("Төбе жойылды.")
            elif choice == "9":
                graph.save(DATA_FILE); print("JSON сақталды:", DATA_FILE)
            elif choice == "10":
                graph.load(DATA_FILE); print("JSON қайта жүктелді.")
            else:
                print("Мәзірден 0–10 аралығындағы нөмірді таңдаңыз.")
        except (ValueError, KeyError, OSError) as exc:
            print("ҚАТЕ:", exc)

if __name__ == "__main__":
    main()
