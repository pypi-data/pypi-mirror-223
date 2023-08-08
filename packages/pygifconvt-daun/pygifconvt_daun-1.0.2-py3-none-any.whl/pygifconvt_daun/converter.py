import glob
from PIL import Image

# 패키지로 만들기
class Gifconverter:
    def __init__(self, path_in=None, path_out=None, resize=(320,240)):
        '''
            path_in : 원본이미지 경로
            path_out : 결과 이미지 경로
            resize : 리사이징 크기
        '''
        self.path_in = path_in or './*.png'
        self.path_out = path_out or './output.gif'
        self.resize = resize

    def convert_gif(self):
        '''
        GIF 이미지 변환기능 수행
        '''
        print(self.path_in, self.path_out, self.resize)

        img, *imges = \
        [Image.open(f).resize(self.resize) for f in sorted(glob.glob(self.path_in))]

        try:
            img.save(
                fp = self.path_out,
                format='GIF',
                append_images = imges,
                save_all = True,
                duration = 500,
                loop = 0
            )
        except IOError:
            print('Cannot Convert!', img)

# 메인일 경우에만 실행한다.
if __name__ == '__main__':
    c = Gifconverter('./images/*.png', './image_out/result7.gif')
    c.convert_gif()
