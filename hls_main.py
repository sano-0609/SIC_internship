# -*- coding: utf-8 -*-
import sys, os
import subprocess
import codecs

def create_hls():
    # 高画質m3u8の作成 (input.mp4 -> hls/h.m3u8)
    c = 'ffmpeg'
    c += ' -i sample_video.mp4'
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 5'
    c += ' -segment_list hls/h.m3u8'
    c += ' hls/h_%5d.ts'
    code = subprocess.call(c.split())
    print('process=' + str(code))

    # 低画質mp4の作成 (input.mp4 -> input_low.mp4)
    c = 'ffmpeg'
    c += ' -i sample_video.mp4'
    c += ' -f mp4 -vcodec h264 -vb 500k -s 640x360 -pix_fmt yuv420p'
    c += ' -ac 2 -ar 48000 -ab 128k -acodec aac -strict experimental'
    c += ' -movflags faststart'
    c += ' sample_video_low.mp4'
    code = subprocess.call(c.split())
    print('process=' + str(code))

    # 低画質m3u8の作成 (input_low.mp4 -> hls/l.m3u8)
    c = 'ffmpeg'
    c += ' -i sample_video_low.mp4'
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 5'
    c += ' -segment_list hls/l.m3u8'
    c += ' hls/l_%5d.ts'
    code = subprocess.call(c.split())
    print('process=' + str(code))

    # 低画質高画質を含めたm3u8の作成 (->hls/playlist.m3u8)
    t = '#EXTM3U'
    t += '\n##EXT-X-VERSION:3'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=500000'
    t += '\nl.m3u8'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=4000000'
    t += '\nh.m3u8'
    f = codecs.open('hls/playlist.m3u8', 'w', 'utf-8')
    f.write(t)
    f.close()

if __name__ == "__main__":
    create_hls()