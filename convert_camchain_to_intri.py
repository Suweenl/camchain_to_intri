import yaml
import argparse
import re
import os

def extract_cam_blocks_from_file(file_path):
    with open(file_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ Skipping {file_path}, failed to parse YAML: {e}")
            return {}
    return {k: v for k, v in data.items() if re.match(r'^cam\d+$', k)}

def load_cam_name_mapping(config_path):
    if config_path is None:
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def convert_camchain_to_opencv_yaml_auto_names(input_path, output_path, config_path=None):
    cam_name_map = load_cam_name_mapping(config_path)

    all_cam_blocks = {}

    # Determine if the input is a directory or file
    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(input_path, filename)
                cam_blocks = extract_cam_blocks_from_file(filepath)
                all_cam_blocks.update(cam_blocks)
    else:
        all_cam_blocks = extract_cam_blocks_from_file(input_path)

    if not all_cam_blocks:
        print("❌ No camX data found.")
        return

    camera_names = []
    cam_outputs = []

    for cam_key, cam in all_cam_blocks.items():
        mapped_name = cam_name_map.get(cam_key, cam.get("name", cam_key))  # Prefer config name > "name" field > camX

        intrinsics = cam.get("intrinsics", [])
        distortion = cam.get("distortion_coeffs", [])
        distortion.append(0.000000)

        if len(intrinsics) != 4:
            print(f"⚠️ Skipping {cam_key}: intrinsics length is not 4.")
            continue

        fx, fy, cx, cy = intrinsics
        K = [
            fx, 0.0, cx,
            0.0, fy, cy,
            0.0, 0.0, 1.0
        ]

        camera_names.append(f"{mapped_name}")
        cam_outputs.append({
            "name": mapped_name,
            "K": K,
            "distortion": distortion
        })

    with open(output_path, 'w') as f:
        f.write("%YAML:1.0\n---\n")
        f.write("names:\n")
        for name in camera_names:
            f.write(f"  - \"{name}\"\n")

        for cam in cam_outputs:
            name = cam["name"]
            K = cam["K"]
            distortion = cam["distortion"]
            f.write(f"K_{name}: !!opencv-matrix\n")
            f.write("  rows: 3\n")
            f.write("  cols: 3\n")
            f.write("  dt: d\n")
            f.write("  data: [" + ", ".join(f"{v:.6f}" for v in K) + "]\n")

            f.write(f"dist_{name}: !!opencv-matrix\n")
            f.write("  rows: 1\n")
            f.write(f"  cols: {len(distortion)}\n")
            f.write("  dt: d\n")
            f.write("  data: [" + ", ".join(f"{v:.6f}" for v in distortion) + "]\n")

    print(f"✅ Conversion completed. {len(camera_names)} camera(s) written to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert camchain.yaml or folder into OpenCV-style intrinsics YAML")
    parser.add_argument("input", help="Input: a camchain.yaml file or a folder with YAML files")
    parser.add_argument("output", help="Output: OpenCV-style intrinsics YAML file")
    parser.add_argument("--config", help="Optional config.yaml to map camX to real camera IDs", default=None)
    args = parser.parse_args()

    convert_camchain_to_opencv_yaml_auto_names(args.input, args.output, args.config)
