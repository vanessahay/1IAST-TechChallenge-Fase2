import subprocess
import json
import sys
import os

GSLIDES = "/google/bin/releases/gemini-agents-gslides/gslides"
PARSE_DSL = "/usr/local/google/home/vanessahay/latam-agents-and-skills/skills/internal/cloudstyle-slides/scripts/parse_dsl.py"
DECK_DSL = "/usr/local/google/home/vanessahay/aulao/1IAST-TechChallenge-Fase2/apresentacao.md"

def run_cmd(args):
    result = subprocess.run([GSLIDES] + args, capture_output=True, text=True, check=True)
    return result.stdout

def main():
    # 1. Parse DSL to JSON
    print("Parsing DSL...")
    try:
        dsl_json_str = subprocess.run(["python3", PARSE_DSL, DECK_DSL], capture_output=True, text=True, check=True).stdout
        dsl_data = json.loads(dsl_json_str)
    except Exception as e:
        print(f"Error parsing DSL: {e}")
        sys.exit(1)
        
    slides_data = dsl_data["slides"]
    print(f"Parsed {len(slides_data)} slides.")

    # 2. Create Presentation
    print("Creating new presentation...")
    try:
        create_out = run_cmd(["create", "1IAST - Tech Challenge Fase 2 - Apresentacao", "--json"])
        parts = create_out.strip().split("ID: ")
        if len(parts) < 2:
            try:
                data = json.loads(create_out)
                pres_id = data["presentationId"]
            except:
                raise Exception(f"Failed to parse ID from output: {create_out}")
        else:
            pres_id = parts[1].replace(")", "")
            
        pres_url = f"https://docs.google.com/presentation/d/{pres_id}"
        print(f"Created presentation ID: {pres_id}")
        print(f"URL: {pres_url}")
    except Exception as e:
        print(f"Error creating presentation: {e}")
        if hasattr(e, "stderr") and e.stderr:
            print(f"CLI Error: {e.stderr}")
        sys.exit(1)

    # 3. Build Batch Operations
    batch_ops = []
    
    # Colors Palette (Cloudstyle-like)
    colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853"] # Blue, Red, Yellow, Green
    ink_color = "#202124"
    body_color = "#5F6368"
    white_color = "#FFFFFF"

    print("Generating batch operations...")
    for idx, slide in enumerate(slides_data):
        stype = slide["type"]
        
        # We use slide index 0 (which is created by default and has ID "p") for the first slide (title)
        # For all others, we add a BLANK slide.
        if idx == 0:
            sid = "p"
            title_text = slide["headline"]
            subtitle_text = slide["date"]
            
            batch_ops.append({
                "op": "insert-text",
                "element": "i0",
                "text": title_text
            })
            batch_ops.append({
                "op": "style-text",
                "element": "i0",
                "font_family": "Google Sans",
                "font_size": 40,
                "bold": True,
                "color": ink_color
            })
            
            batch_ops.append({
                "op": "insert-text",
                "element": "i1",
                "text": subtitle_text
            })
            batch_ops.append({
                "op": "style-text",
                "element": "i1",
                "font_family": "Google Sans Text",
                "font_size": 16,
                "color": body_color
            })
            continue

        sid = f"slide_{idx}"
        batch_ops.append({
            "op": "add-slide",
            "id": sid,
            "layout": "BLANK"
        })
        
        # Add Title (except for section and closing)
        if stype not in ["section", "closing"]:
            title_id = f"title_{idx}"
            batch_ops.append({
                "op": "add-textbox",
                "slide": sid,
                "id": title_id,
                "text": slide.get("title", ""),
                "x": 36,
                "y": 40,
                "width": 648,
                "height": 50
            })
            batch_ops.append({
                "op": "style-text",
                "element": title_id,
                "font_family": "Google Sans",
                "font_size": 28,
                "bold": True,
                "color": ink_color
            })
            
            # Add Footer
            footer_id = f"footer_{idx}"
            batch_ops.append({
                "op": "add-textbox",
                "slide": sid,
                "id": footer_id,
                "text": "1IAST - Tech Challenge Fase 2 | Grupo 1IAST - FIAP",
                "x": 36,
                "y": 375,
                "width": 648,
                "height": 20
            })
            batch_ops.append({
                "op": "style-text",
                "element": footer_id,
                "font_family": "Google Sans Text",
                "font_size": 8,
                "color": body_color
            })

        # Add content based on slide type
        if stype == "contents":
            body_id = f"body_{idx}"
            
            list_lines = []
            for i, bullet in enumerate(slide["bullets"]):
                list_lines.append(f"0{i+1}\t{bullet}")
            list_text = "\n".join(list_lines)
            
            batch_ops.append({
                "op": "add-textbox",
                "slide": sid,
                "id": body_id,
                "text": list_text,
                "x": 36,
                "y": 110,
                "width": 648,
                "height": 250
            })
            batch_ops.append({
                "op": "style-text",
                "element": body_id,
                "font_family": "Google Sans",
                "font_size": 16,
                "color": ink_color
            })
            
            current_pos = 0
            for i, line in enumerate(list_lines):
                batch_ops.append({
                    "op": "style-text",
                    "element": body_id,
                    "bold": True,
                    "color": colors[0], # Blue
                    "start": current_pos,
                    "end": current_pos + 2
                })
                current_pos += len(line) + 1

        elif stype == "section":
            num_id = f"sec_num_{idx}"
            title_id = f"sec_title_{idx}"
            sub_id = f"sec_sub_{idx}"
            
            # Big Number
            batch_ops.append({
                "op": "add-textbox",
                "slide": sid,
                "id": num_id,
                "text": slide.get("number", "01"),
                "x": 36,
                "y": 96,
                "width": 240,
                "height": 130
            })
            batch_ops.append({
                "op": "style-text",
                "element": num_id,
                "font_family": "Google Sans",
                "font_size": 90,
                "bold": True,
                "color": colors[0]
            })
            
            # Title
            batch_ops.append({
                "op": "add-textbox",
                "slide": sid,
                "id": title_id,
                "text": slide.get("title", ""),
                "x": 36,
                "y": 232,
                "width": 640,
                "height": 60
            })
            batch_ops.append({
                "op": "style-text",
                "element": title_id,
                "font_family": "Google Sans",
                "font_size": 32,
                "bold": True,
                "color": ink_color
            })
            
            # Subhead
            if "subhead" in slide:
                batch_ops.append({
                    "op": "add-textbox",
                    "slide": sid,
                    "id": sub_id,
                    "text": slide["subhead"],
                    "x": 36,
                    "y": 300,
                    "width": 640,
                    "height": 30
                })
                batch_ops.append({
                    "op": "style-text",
                    "element": sub_id,
                    "font_family": "Google Sans Text",
                    "font_size": 16,
                    "color": body_color
                })

        elif stype == "bullets":
            body_id = f"body_{idx}"
            body_text = "\n".join([f"•  {b}" for b in slide["bullets"]])
            
            batch_ops.append({
                "op": "add-textbox",
                "slide": sid,
                "id": body_id,
                "text": body_text,
                "x": 36,
                "y": 110,
                "width": 648,
                "height": 250
            })
            batch_ops.append({
                "op": "style-text",
                "element": body_id,
                "font_family": "Google Sans Text",
                "font_size": 16,
                "color": body_color
            })

        elif stype == "flow":
            steps = [row[0] for row in slide["rows"]]
            N = len(steps)
            boxw = int((648 - (N - 1) * 30) / N)
            y = 170
            h = 90
            
            for i, step in enumerate(steps):
                x = 36 + i * (boxw + 30)
                box_id = f"flow_{idx}_step_{i}"
                
                batch_ops.append({
                    "op": "add-textbox",
                    "slide": sid,
                    "id": box_id,
                    "text": step,
                    "x": x,
                    "y": y,
                    "width": boxw,
                    "height": h,
                    "color": white_color,
                    "bold": True,
                    "font_size": 10,
                    "background_color": colors[i % len(colors)]
                })
                batch_ops.append({
                    "op": "style-text",
                    "element": box_id,
                    "font_family": "Google Sans",
                    "color": white_color
                })
                
                if i < N - 1:
                    arrow_id = f"flow_{idx}_arrow_{i}"
                    batch_ops.append({
                        "op": "add-textbox",
                        "slide": sid,
                        "id": arrow_id,
                        "text": "→",
                        "x": x + boxw + 6,
                        "y": y + 34,
                        "width": 18,
                        "height": 24
                    })
                    batch_ops.append({
                        "op": "style-text",
                        "element": arrow_id,
                        "font_family": "Google Sans",
                        "font_size": 18,
                        "bold": True,
                        "color": body_color
                    })

        elif stype == "comparison":
            cols = slide["rows"]
            N = len(cols)
            colw = int(648 / N)
            
            for i, col in enumerate(cols):
                heading = col[0]
                body_bullets = col[1].split(";")
                x = 36 + i * colw
                
                head_id = f"comp_{idx}_head_{i}"
                body_id = f"comp_{idx}_body_{i}"
                
                batch_ops.append({
                    "op": "add-textbox",
                    "slide": sid,
                    "id": head_id,
                    "text": heading,
                    "x": x,
                    "y": 110,
                    "width": colw - 20,
                    "height": 30
                })
                batch_ops.append({
                    "op": "style-text",
                    "element": head_id,
                    "font_family": "Google Sans",
                    "font_size": 16,
                    "bold": True,
                    "color": colors[i % len(colors)]
                })
                
                body_text = "\n".join([f"•  {b.strip()}" for b in body_bullets])
                batch_ops.append({
                    "op": "add-textbox",
                    "slide": sid,
                    "id": body_id,
                    "text": body_text,
                    "x": x,
                    "y": 150,
                    "width": colw - 20,
                    "height": 200
                })
                batch_ops.append({
                    "op": "style-text",
                    "element": body_id,
                    "font_family": "Google Sans Text",
                    "font_size": 13,
                    "color": "#3C4043"
                })

        elif stype == "stats":
            stats_list = slide["rows"]
            N = len(stats_list)
            boxw = 196
            spacing = 30
            
            for i in range(min(N, 3)):
                val = stats_list[i][0]
                lbl = stats_list[i][1]
                cell_text = f"{val}\n{lbl}"
                x = 36 + i * (boxw + spacing)
                cell_id = f"stats_{idx}_cell_{i+1}"
                
                batch_ops.append({
                    "op": "add-textbox",
                    "slide": sid,
                    "id": cell_id,
                    "text": cell_text,
                    "x": x,
                    "y": 170,
                    "width": boxw,
                    "height": 150
                })
                
                batch_ops.append({
                    "op": "style-text",
                    "element": cell_id,
                    "font_family": "Google Sans",
                    "bold": True,
                    "font_size": 44,
                    "color": colors[i % len(colors)],
                    "start": 0,
                    "end": len(val)
                })
                batch_ops.append({
                    "op": "style-text",
                    "element": cell_id,
                    "font_family": "Google Sans Text",
                    "bold": False,
                    "font_size": 12,
                    "color": "#71717A",
                    "start": len(val) + 1,
                    "end": len(cell_text)
                })

        elif stype == "closing":
            title_id = f"closing_title_{idx}"
            batch_ops.append({
                "op": "add-textbox",
                "slide": sid,
                "id": title_id,
                "text": slide["headline"],
                "x": 36,
                "y": 140,
                "width": 648,
                "height": 100
            })
            batch_ops.append({
                "op": "style-text",
                "element": title_id,
                "font_family": "Google Sans",
                "font_size": 44,
                "bold": True,
                "color": ink_color
            })

    # 4. Save Batch Operations to File
    batch_file = "/tmp/batch_ops_b.json"
    with open(batch_file, "w", encoding="utf-8") as f:
        json.dump(batch_ops, f, indent=2, ensure_ascii=False)

    # 5. Execute Batch Update
    print("Executing batch update on Google Slides...")
    try:
        batch_out = run_cmd(["batch", pres_id, "--file", batch_file])
        print("Batch execution successful!")
    except Exception as e:
        print(f"Error during batch execution: {e}")
        if hasattr(e, "stderr") and e.stderr:
            print(f"CLI Error: {e.stderr}")
        sys.exit(1)

    print("\n--- PRESENTATION BUILT SUCCESSFULLY! ---")
    print(f"Presentation URL: {pres_url}")

if __name__ == "__main__":
    main()
