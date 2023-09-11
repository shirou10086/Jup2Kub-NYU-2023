import subprocess
import time

def get_docker_images():
    try:
        result = subprocess.run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"], check=True, stdout=subprocess.PIPE, text=True)
        
        image_names = set(result.stdout.strip().split("\n"))
        return image_names

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while fetching Docker images: {e}")
        print(e.stderr)
        return set()

def compare_docker_images(initial_images, final_images):
    # 使用集合
    new_images = final_images - initial_images

    if new_images:
        print("New Docker images:")
        for img in new_images:
            print(img)
    else:
        print("No new Docker images found.")

if __name__ == "__main__":
    print("Fetching initial Docker images list...")
    initial_images = get_docker_images()

    time.sleep(30)

    print("\nFetching Docker images list again...")
    final_images = get_docker_images()

    compare_docker_images(initial_images, final_images)
