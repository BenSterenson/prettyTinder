import os
import urllib


class PhotoDownloader(object):


    def __init__(self, img_arr=[], photo_path_output=os.getcwd(), face_landmark_img_exe='',):
        self.img_arr = img_arr
        self.face_landmark_img_exe = face_landmark_img_exe

        self.photo_path_output = os.path.join(photo_path_output, "Tinder_Output")
        
        # runs landmark detection on all images
        self.fdir = os.path.join(self.photo_path_output, "Tinder_Photos")
        self.make_dir(self.fdir)

        # directory where detected landmarks, gaze, and action units should be written
        self.ofdir = os.path.join(self.photo_path_output, "Photos_ofdir")
        self.make_dir(self.ofdir)

        # directory where images with detected landmarks should be stored
        self.oidir = os.path.join(self.photo_path_output, "Photos_oidir")
        self.make_dir(self.oidir)

        # directory where pose files are output (3D landmarks in images together with head pose and gaze)
        self.opdir = os.path.join(self.photo_path_output, "Photos_opdir")
        self.make_dir(self.opdir)
    
    def make_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def download_all_photos(self):
        photo_count = 0
        for img_url in self.img_arr:
            urllib.urlretrieve(img_url, os.path.join(self.fdir, str(photo_count) + ".jpg"))
            photo_count += 1

    def photo_analysis(self):
        cmd = '"{0}" -fdir "{1}" -ofdir "{2}" -oidir "{3}" -opdir "{4}"'.format(self.face_landmark_img_exe, self.fdir, self.ofdir, self.oidir, self.opdir)
        print cmd
        os.system(cmd)
        x=5

    def start(self):
        self.download_all_photos()
        self.photo_analysis()

arr = ["https://images-ssl.gotinder.com/5a22d45f7a77a8d70303182c/640x640_a4997534-d6a9-4081-9fb3-7683f88fd71f.jpg",
        "https://images-ssl.gotinder.com/5a22d45f7a77a8d70303182c/640x640_8ef4262a-1dd5-4573-9457-bf8651116a6d.jpg",
        "https://images-ssl.gotinder.com/5a22d45f7a77a8d70303182c/640x640_0c3af107-e2c5-4c7d-bc05-b84045436d4d.jpg"]



arr2 = ["https://images-ssl.gotinder.com/5a230fe79c3119087d3eda39/640x640_d4912077-84f8-4068-ba1d-3550079742a7.jpg",
        "https://images-ssl.gotinder.com/5a230fe79c3119087d3eda39/640x640_bf4d9d55-a868-4d5b-8ead-50d42871187e.jpg",
        "https://images-ssl.gotinder.com/5a230fe79c3119087d3eda39/640x640_d8df634c-e18a-4bda-8821-e7261a7cb787.jpg",
        "https://images-ssl.gotinder.com/5a230fe79c3119087d3eda39/640x640_78eeef08-8ccb-4b2e-9a2e-1da4eb5cd535.jpg"]  

face_landmark_img_exe = os.path.join(os.getcwd(), 'OpenFace_0.2.4_win_x64', 'FaceLandmarkImg.exe')
photo_downloader = PhotoDownloader(img_arr=arr2, face_landmark_img_exe=face_landmark_img_exe)
photo_downloader.start()