from fastapi import FastAPI, HTTPException, Path
import subprocess
from .schemas import OrbSlamRequest
from .bundles import read_bind_rows, procesar_datos, generate_image_table, write_in_folder
from .functions import video_to_frame, get_best_triangulacion, csv_to_ply_with_sphere, get_best_triangulacion2
import sys
import os


print("Python ejecutado:", sys.executable)
print("Directorio actual:", os.getcwd())
print("Archivos en el directorio actual:", os.listdir("."))

app = FastAPI()

@app.get("/")
async def root():
    return {"message: hola como estamos"}

# EP01 - ORB SLAM y Generación de nube 3D
@app.post('/orb_run')
async def orb_run(request: OrbSlamRequest):
    
    try: 
        
        # Creamos la carpeta del video
        
        folder_path = os.path.join(request.output_path, request.video_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Carpeta creada: {folder_path}")
        else:
            print(f"La carpeta ya existe: {folder_path}")
            
        # Generamos bundles.csv
        
        tracker_detection_path = os.path.join(request.input_path, request.video_name+'_detections.csv')
        qr_detection_path = os.path.join(request.input_path, request.video_name+'_qr_detections.csv')
        
        path_list = [tracker_detection_path, qr_detection_path]

        df = read_bind_rows(path_list)
        df = procesar_datos(df, 'baya')
        df = generate_image_table(df, baya_thresh=request.baya_threshold, qr_thresh=request.qr_threshold)
        write_in_folder(df, folder=folder_path)
        
        # Generamos los frames a partir del video. 
        # RECORDAR: El ID del racimo está hardcode en la función video_to_frame
        
        video_path = os.path.join(request.input_path, request.video_name+'.mp4')
        output_frames = os.path.join(folder_path, 'frames')

        # Elimino el ./ del inicio de la ruta del video
        video_path = video_path.replace('./', '') if video_path.startswith('./') else video_path

        video_to_frame(video_path, output_frames, request.video_name)

        # RECONSTRUCCIÓN DE BAYAS
        
        # Si /calib está en la carpeta /input
        calib_path = os.path.join(request.input_path, 'calib', request.calib_file)
        
        # Si bundles.csv está en /output 
        bundles_path = os.path.join(folder_path, 'bundles.csv')
        
        # Si frames están en /input/frames
        frames_path = os.path.join(folder_path, 'frames')
        
        print("Iniciando triangulación...")
        # Elegimos cuál es la mejor reconstrucción
        path_minimo, mer_minimo, dist_minimo = get_best_triangulacion(output_path=folder_path, 
                                                                        dists_list=request.dists_list, 
                                                                        min_mer=request.min_mer, 
                                                                        min_dist=request.min_dist, 
                                                                        min_path=request.min_path, 
                                                                        input_csv_name=request.reproy_csv_name,
                                                                        calib_path=calib_path,
                                                                        bundles_path=bundles_path,
                                                                        frames_path=frames_path,
                                                                        qr_dist=request.qr_dist
                                                                    )
        
        print("El mejor path es:", path_minimo)
        print("El mejor mer es:", mer_minimo)
        print("La mejor distancia es:", dist_minimo)
        
        # Generamos el CSV a PLY
        
        print("Generando nube de puntos...")
        
        ply_file = os.path.join(folder_path, 'nube.ply')
        
        csv_to_ply_with_sphere(path_minimo, ply_file, num_points=100)
        
        print("Listo!")
        
        return {
            "success": True
            # "output": result.stdout,
            # "error": result.stderr
        }

    except subprocess.CalledProcessError as e:
        
        detalles = {
            "error": "Error con triangulacion de bayas",
            "command": e.args,
            "exit_code": e.returncode, 
            "stdout": e.stdout,
            "stderr": e.stderr
        }
        
        raise HTTPException(status_code=400, detail=detalles)

@app.get('/minim-path')
async def ratio_minimo(request: OrbSlamRequest): 
    
    folder_path = os.path.join(request.output_path, request.video_name)
    
    path_minimo, mer_minimo, dist_minimo = get_best_triangulacion2(
        output_path=folder_path,
        dists_list=request.dists_list,
        min_mer=request.min_mer,
        min_dist=request.min_dist,
        min_path=request.min_path,
        input_csv_name=request.reproy_csv_name
    )
    
    return {
                "path_minimo": path_minimo,
                "mer_minimo": mer_minimo,
                "dist_minimo": dist_minimo,
            }
