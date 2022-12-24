#!/bin/env python
import time
import sys
import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from threading import Thread
cwd = sys.argv[0]
if '/' in cwd:
    mvwd = cwd.split('pi_subway.py')[0]
    os.chdir(mvwd)

sys.path.append('additional_pyy_files')    
import additional_py_files.subway_connect as sc
import additional_py_files.common as common


class draw():
    def local_train(self, canvas,  x, y, color):
        graphics.DrawLine(canvas, x+2, y+0, x+6, y+0, color)
        graphics.DrawLine(canvas, x+1, y+1, x+7, y+1, color)
        graphics.DrawLine(canvas, x+0, y+2, x+8, y+2, color)
        graphics.DrawLine(canvas, x+0, y+3, x+8, y+3, color)
        graphics.DrawLine(canvas, x+0, y+4, x+8, y+4, color)
        graphics.DrawLine(canvas, x+0, y+5, x+8, y+5, color)
        graphics.DrawLine(canvas, x+0, y+6, x+8, y+6, color)
        graphics.DrawLine(canvas, x+1, y+7, x+7, y+7, color)
        graphics.DrawLine(canvas, x+2, y+8, x+6, y+8, color)

    def express_train(self, canvas,  x, y, color):
        # Draw circle with lines
        graphics.DrawLine(canvas, x+4, y+0, x+4, y+0, color)
        graphics.DrawLine(canvas, x+3, y+1, x+5, y+1, color)
        graphics.DrawLine(canvas, x+2, y+2, x+6, y+2, color)
        graphics.DrawLine(canvas, x+1, y+3, x+7, y+3, color)
        graphics.DrawLine(canvas, x+0, y+4, x+8, y+4, color)
        graphics.DrawLine(canvas, x+1, y+5, x+7, y+5, color)
        graphics.DrawLine(canvas, x+2, y+6, x+6, y+6, color)
        graphics.DrawLine(canvas, x+3, y+7, x+5, y+7, color)
        graphics.DrawLine(canvas, x+4, y+8, x+4, y+8, color)

class nyc_subway():
    
    def run(self):
        self.configs()
        Thread(target = self.data_pull).start()
        Thread(target = self.display).start()
        
    def data_pull(self):
        while True:
            try:
                data = sc.all_train_data()
                trains = sc.next_train_in(self.station,data)
                trains.sort(key=lambda k : k['arrival'])
                trains = trains[0:4]
                for x in trains:
                    common.log_add(str(x),'Display',2)
                self.train_1 = trains[0]['route']
                self.train_1_time = (trains[0]['arrival'])
                self.train_1_direction = trains[0]['final_dest']
                self.train_2 = trains[1]['route']
                self.train_2_time = (trains[1]['arrival'])
                self.train_2_direction = trains[1]['final_dest']
                self.train_3 = trains[2]['route']
                self.train_3_time = (trains[2]['arrival'])
                self.train_3_direction = trains[2]['final_dest']
                self.train_4 = trains[3]['route']
                self.train_4_time = (trains[3]['arrival'])
                self.train_4_direction = trains[3]['final_dest']
                self.station_load()
            except Exception as error:
                note = str(error)
                common.log_add(note,'Display',1)
                self.general_error('Error Loading','Data')
                self.station_load()
            
    def location_restart(self):
        self.add_number_1 = -1
        self.add_number_2 = -1
        self.add_number_3 = -1
        self.add_number_4 = -1
        

    def display(self):
        first_2 = True
        while True:
            for i in range(35):
                self.station_load()
                self.canvas.Clear()
                self.textColor = graphics.Color(237, 234, 222)

                graphics.DrawText(self.canvas, 
                                self.font, 
                                self.station_pos, 
                                7, 
                                self.waiting_color, 
                                self.station)
        
                if len(self.station) >= 16:
                    if int(self.station_pos) == 64:
                        time.sleep(5)
                        self.station_pos -= 1
                    elif self.station_pos > (65 - len(self.station)):
                        self.station_pos -= 1
                    elif self.station_pos == (65 - len(self.station)):
                        self.station_pos = 65
                        self.location_restart()
                else:
                    self.station_pos = 65
                
                if first_2 is True:
                    self.train_dispaly(self.train_1,
                                    self.train_1_time,
                                    self.train_1_direction,
                                    True,
                                    )
                    
                    self.train_dispaly(self.train_2,
                                    self.train_2_time,
                                    self.train_2_direction,
                                    False,
                                    )
                if first_2 is False:
                    self.train_dispaly(self.train_3,
                                    self.train_3_time,
                                    self.train_3_direction,
                                    True,
                                    )
                    
                    self.train_dispaly(self.train_4,
                                    self.train_4_time,
                                    self.train_4_direction,
                                    False,
                                    )
                time.sleep(.7)
                self.canvas = self.matrix.SwapOnVSync(self.canvas)
            if first_2 is True:
                first_2 = False
                self.location_restart()
            elif first_2 is False:
                first_2 = True
                self.location_restart()

    def train_dispaly(self,train,train_time,direction,top):

        line_draw = draw()
        
        if top is True:
            add_number = self.add_number_1
            height = 17
        elif top is False:
            add_number = self.add_number_2
            height = 27    
        time = (str(train_time) + 'min')
        circle_color = self.train_colors(train)
        text_color = self.waiting_color
        
        if len(train) == 1:
            local = True
        else:
            local = False
        
        if local is True:
            if top is True:
                line_draw.local_train(self.canvas, 64, 10, circle_color)
                graphics.DrawText(self.canvas, self.font, 67, height, self.in_circle_color, train)
            if top is False:
                line_draw.local_train(self.canvas, 64, 20, circle_color)
                graphics.DrawText(self.canvas, self.font, 67, height, self.in_circle_color, train)
        
        if local is False:
            if top is True:
                line_draw.express_train(self.canvas, 64, 10, circle_color)
                graphics.DrawText(self.canvas, self.font, 67, height, self.in_circle_color, train)
            if top is False:
                line_draw.express_train(self.canvas, 64, 20, circle_color)
                graphics.DrawText(self.canvas, self.font, 67, height, self.in_circle_color, train)
        
        if train_time == 0:
            text_color = self.arrival_color
        elif len(time) == 4:
            graphics.DrawText(self.canvas, self.font, 112, height, text_color, time)
            text_color = self.waiting_color 
        elif len(time) == 5:
            graphics.DrawText(self.canvas, self.font, 109, height, text_color, time)
             
        if train_time == 0 or train_time == '':
            if len(direction) > 13:
                start_number = 0
                end_number = 13
                if (end_number + add_number) < (len(direction) + 13):
                    print_text = direction[(start_number + add_number):(end_number + add_number)]
                    graphics.DrawText(self.canvas, self.font, 74, height, text_color, print_text)

                    if top is True:
                        self.add_number_1 += 1
                    if top is False:
                        self.add_number_2 += 1
                else: 
                    print_text = direction[(start_number + add_number):(end_number + add_number)]
                    graphics.DrawText(self.canvas, self.font, 74, height, text_color, print_text)
                    if top is True:
                        self.add_number_1 = 0
                    if top is False:
                        self.add_number_2 = 0
            else:
                graphics.DrawText(self.canvas, self.font, 74, height, text_color, direction)
                
        else:
            if len(direction) > 8:
                if train_time == 0:
                    start_number = 0
                    end_number = 13
                    if (end_number + add_number) < (len(direction) + 13):
                        print_text = direction[(start_number + add_number):(end_number + add_number)]
                        graphics.DrawText(self.canvas, self.font, 74, height, text_color, print_text)

                        if top is True:
                            self.add_number_1 += 1
                        if top is False:
                            self.add_number_2 += 1
                    else: 
                        print_text = direction[(start_number + add_number):(end_number + add_number)]
                        graphics.DrawText(self.canvas, self.font, 74, height, text_color, print_text)
                        if top is True:
                            self.add_number_1 = 0
                        if top is False:
                            self.add_number_2 = 0
                    
                else:
                    start_number = 0
                    end_number = 8
                    if (end_number + add_number) < (len(direction) + 8):
                        print_text = direction[(start_number + add_number):(end_number + add_number)]
                        graphics.DrawText(self.canvas, self.font, 74, height, text_color, print_text)

                        if top is True:
                            self.add_number_1 += 1
                        if top is False:
                            self.add_number_2 += 1
                    else: 
                        print_text = direction[(start_number + add_number):(end_number + add_number)]
                        graphics.DrawText(self.canvas, self.font, 74, height, text_color, print_text)
                        if top is True:
                            self.add_number_1 = 0
                        if top is False:
                            self.add_number_2 = 0            
            else:
                graphics.DrawText(self.canvas, self.font, 74, height, text_color, direction)


    def configs(self):
        self.previous_station = ''
        self.station_load()
        #self.train_loading()
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.cols = 64
        self.options.chain_length = 2
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat'
        self.matrix = RGBMatrix(options=self.options)
        self.font = graphics.Font()
        self.arrival_color = graphics.Color(237, 132, 40)
        self.waiting_color = graphics.Color(0, 147, 60)
        self.in_circle_color = graphics.Color(0, 0, 0)
        self.error_color = graphics.Color(255,0,0)
        self.font.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf') 
        self.canvas = self.matrix.CreateFrameCanvas() 
        self.station_pos = 65
        note = 'Loaded Configs'
        common.log_add(note,'Display',2)

    def train_colors(self,train):
        if train in ['A','C','E']:
            return graphics.Color(0,57,166) 
        elif train in ['B','D','F','FX','M']:
            return graphics.Color(255,99,25)
        elif train in ['G','GS']:
            return graphics.Color(108, 190, 69)
        elif train in ['J','Z']:
            return graphics.Color(153, 102, 51)
        elif train in ['L']:
            return graphics.Color(167, 169, 172)
        elif train in ['N','Q','R','W']:
            return  graphics.Color(252, 204, 10)
        elif train in ['S']:
            return graphics.Color(128, 129, 131)
        elif train in ['1','2','3']:
            return graphics.Color(238, 53, 46)
        elif train in ['4','5','6','6X']:
            return graphics.Color(0, 147, 60)
        elif train in ['7','7X']:
            return graphics.Color(185, 51, 173)
        elif train in ['T']:
            return graphics.Color(0, 173, 208)
        elif train in ['!']:
            return graphics.Color(255,0,0)
        elif train == '':
            return graphics.Color(0, 0, 0)
        else:
            note = train + 'Color load error'
            common.log_add(note,'Display',1)
            return graphics.Color(0, 0, 0)
        
    def station_load(self):
        new_station = common.config_return('station')
        if new_station != self.previous_station:
            station_check = common.station_check(new_station)
            if station_check is True:
                self.station = new_station
                self.previous_station = new_station
                self.train_loading()
                self.station_pos = 65
                note = 'New Station: ' + self.station
                common.log_add(note,'Display',2)
            else:
                self.general_error('Check station','spelling')
        else:
            note = 'No Station Change'
            common.log_add(note,'Display',4)
        
    def general_error(self,line_1,line_2):
        self.station = 'Error!!!'
        self.train_1 = '!'
        self.train_1_time = ''
        self.train_1_direction = line_1
        self.train_2 = '!'
        self.train_2_time = ''
        self.train_2_direction = line_2
        self.train_3 = '!'
        self.train_3_time = ''
        self.train_3_direction = line_1
        self.train_4 = '!'
        self.train_4_time = ''
        self.train_4_direction = line_2
        self.add_number_1 = 0
        self.add_number_2 = 0
        self.add_number_3 = 0
        self.add_number_4 = 0
        
        note = 'Error Loading Train Info, retrying in 15 seconds'
        common.log_add(note,'Display',1)
        time.sleep(15)
        note = 'Reattempting station load'
        common.log_add(note,'Display',4)
        self.station_load()
            
    def train_loading(self):
        self.train_1 = ''
        self.train_1_time = ''
        self.train_1_direction = 'Loading...'
        self.train_2 = ''
        self.train_2_time = ''
        self.train_2_direction = 'Loading...'
        self.train_3 = ''
        self.train_3_time = ''
        self.train_3_direction = 'Loading...'
        self.train_4 = ''
        self.train_4_time = ''
        self.train_4_direction = 'Loading...'
        self.add_number_1 = 0
        self.add_number_2 = 0
        self.add_number_3 = 0
        self.add_number_4 = 0
        note = 'Train Info Loading'
        common.log_add(note,'Display',4)
        
            
        
        


sub = nyc_subway()
sub.run()