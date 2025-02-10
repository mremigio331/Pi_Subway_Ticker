#!/bin/env python
from additional_py_files.pi_board_draw import draw
import additional_py_files.common as common
import additional_py_files.subway_connect as sc
import additional_py_files.constants as constants
import time
import sys
import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from threading import Thread

cwd = sys.argv[0]
if "/" in cwd:
    mvwd = cwd.split(str("/" + os.path.basename(__file__)))[0]
    os.chdir(mvwd)
sys.path.append("additional_py_files")


class nyc_subway:

    def configs(self):
        self.run_status = True
        self.loading = True
        self.previous_station = ""
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.cols = 64
        self.options.chain_length = 2
        self.options.parallel = 1
        self.options.hardware_mapping = "adafruit-hat"
        self.matrix = RGBMatrix(options=self.options)
        self.train_loading()
        self.fonts()
        self.canvas = self.matrix.CreateFrameCanvas()
        self.station_pos = 65
        self.station_load_error = False
        note = "Loaded Configs"
        common.log_add(note, "Display", 2)

    def cycle(self):

        while True:
            cycle_check = common.config_load_v2()["cycle"]
            note = "Cycle is set to " + str(cycle_check)
            common.log_add(note, "System", 1)
            if cycle_check:
                self.cycle_station = sc.random_station_v2()
                note = "Random station selected: " + self.cycle_station
                common.log_add(note, "System", 1)
            sleep_time = common.config_load_v2()["cycle_time"]
            note = f"Cycle time set to {sleep_time} minutes."
            common.log_add(note, "System", 1)
            time.sleep(int(sleep_time) * 60)

    def data_pull(self):
        data_pull_errors = 0
        while True:
            try:
                self.all_train_data = sc.all_train_data()
                trains = sc.next_train_in_v2(self.station, self.all_train_data)
                trains.sort(key=lambda k: k["arrival"])
                trains = trains[0:4]
                for x in trains:
                    common.log_add(str(x), "Display", 3)

                if len(trains) == 4:
                    self.train_1 = trains[0]["route"]
                    self.train_1_time = trains[0]["arrival"]
                    self.train_1_direction = trains[0]["final_dest"]
                    self.train_2 = trains[1]["route"]
                    self.train_2_time = trains[1]["arrival"]
                    self.train_2_direction = trains[1]["final_dest"]
                    self.train_3 = trains[2]["route"]
                    self.train_3_time = trains[2]["arrival"]
                    self.train_3_direction = trains[2]["final_dest"]
                    self.train_4 = trains[3]["route"]
                    self.train_4_time = trains[3]["arrival"]
                    self.train_4_direction = trains[3]["final_dest"]

                elif len(trains) == 3:
                    self.train_1 = trains[0]["route"]
                    self.train_1_time = trains[0]["arrival"]
                    self.train_1_direction = trains[0]["final_dest"]
                    self.train_2 = trains[1]["route"]
                    self.train_2_time = trains[1]["arrival"]
                    self.train_2_direction = trains[1]["final_dest"]
                    self.train_3 = trains[2]["route"]
                    self.train_3_time = trains[2]["arrival"]
                    self.train_3_direction = trains[2]["final_dest"]
                    self.train_4 = ""
                    self.train_4_time = ""
                    self.train_4_direction = ""

                elif len(trains) == 2:
                    self.train_1 = trains[0]["route"]
                    self.train_1_time = trains[0]["arrival"]
                    self.train_1_direction = trains[0]["final_dest"]
                    self.train_2 = trains[1]["route"]
                    self.train_2_time = trains[1]["arrival"]
                    self.train_2_direction = trains[1]["final_dest"]
                    self.train_3 = trains[0]["route"]
                    self.train_3_time = trains[0]["arrival"]
                    self.train_3_direction = trains[0]["final_dest"]
                    self.train_4 = trains[1]["route"]
                    self.train_4_time = trains[1]["arrival"]
                    self.train_4_direction = trains[1]["final_dest"]

                elif len(trains) == 1:
                    self.train_1 = trains[0]["route"]
                    self.train_1_time = trains[0]["arrival"]
                    self.train_1_direction = trains[0]["final_dest"]
                    self.train_2 = ""
                    self.train_2_time = ""
                    self.train_2_direction = ""
                    self.train_3 = trains[0]["route"]
                    self.train_3_time = trains[0]["arrival"]
                    self.train_3_direction = trains[0]["final_dest"]
                    self.train_4 = ""
                    self.train_4_time = ""
                    self.train_4_direction = ""

                else:
                    note = f"{self.station} has no data, loading a new one"
                    common.log_add(note, "System", 2)
                    self.cycle_station = sc.random_station_v2()

                self.loading = False
                self.station_load()
                data_pull_errors = 0

            except Exception as error:
                if data_pull_errors <= 2:
                    data_pull_errors += 1
                    note = str(data_pull_errors) + " errors." + str(error)
                    common.log_add(note, "Display", 1)
                    self.general_error("Error Loading", str(data_pull_errors))
                    self.station_load()
                if data_pull_errors == 3:
                    note = str("Max amount of data_pull_errors reached. Shutting down")
                    common.log_add(note, "Display", 1)
                    self.run_status = False

    def display(self):
        first_2 = True
        while True:
            try:
                for _ in range(35):
                    display_train_string = common.build_station_element(self.station)[
                        "stop_name"
                    ]
                    self.station_load()
                    self.canvas.Clear()
                    self.textColor = graphics.Color(237, 234, 222)
                    if self.loading is True:
                        lines = common.random_trains()
                        self.subway_line_print(lines)
                    else:
                        pass
                    graphics.DrawText(
                        self.canvas,
                        self.font,
                        self.station_pos,
                        7,
                        self.waiting_color,
                        display_train_string,
                    )
                    if len(display_train_string) >= 16:
                        if int(self.station_pos) == 64:
                            time.sleep(5)
                            self.station_pos -= 1
                        elif self.station_pos > (65 - len(display_train_string)):
                            self.station_pos -= 1
                        elif self.station_pos == (65 - len(display_train_string)):
                            self.station_pos = 65
                            self.location_restart()
                    else:
                        self.station_pos = 65
                    if first_2 is True:
                        self.train_display(
                            self.train_1,
                            self.train_1_time,
                            self.train_1_direction,
                            True,
                        )
                        self.train_display(
                            self.train_2,
                            self.train_2_time,
                            self.train_2_direction,
                            False,
                        )
                    if first_2 is False:
                        self.train_display(
                            self.train_3,
                            self.train_3_time,
                            self.train_3_direction,
                            True,
                        )
                        self.train_display(
                            self.train_4,
                            self.train_4_time,
                            self.train_4_direction,
                            False,
                        )
                    time.sleep(1)
                    self.canvas = self.matrix.SwapOnVSync(self.canvas)
                if first_2 is True:
                    first_2 = False
                    self.location_restart()
                elif first_2 is False:
                    first_2 = True
                    self.location_restart()
                else:
                    pass
            except BaseException:
                pass

    def fonts(self):
        self.font = graphics.Font()
        self.arrival_color = graphics.Color(237, 132, 40)
        self.waiting_color = graphics.Color(0, 147, 60)
        self.in_circle_color = graphics.Color(0, 0, 0)
        self.error_color = graphics.Color(255, 0, 0)
        self.font.LoadFont("rgbmatrix/4x6.bdf")

    def general_error(self, line_1, line_2):
        self.station = "Error!!!"
        self.train_1 = "!"
        self.train_1_time = ""
        self.train_1_direction = line_1
        self.train_2 = "!"
        self.train_2_time = ""
        self.train_2_direction = line_2
        self.train_3 = "!"
        self.train_3_time = ""
        self.train_3_direction = line_1
        self.train_4 = "!"
        self.train_4_time = ""
        self.train_4_direction = line_2
        self.add_number_1 = 0
        self.add_number_2 = 0
        self.add_number_3 = 0
        self.add_number_4 = 0

    def location_restart(self):
        self.add_number_1 = -1
        self.add_number_2 = -1
        self.add_number_3 = -1
        self.add_number_4 = -1

    def run(self):
        self.configs()
        self.cycle_station = common.config_load_v2()["station"]
        self.station_load()
        Thread(target=self.data_pull).start()
        Thread(target=self.display).start()
        Thread(target=self.cycle).start()
        Thread(target=self.export_all_data).start()

    def export_all_data(self):
        while self.run_status:
            self.next_four_trains = [
                {
                    "train": self.train_1,
                    "train_time": self.train_1_time,
                    "train_direction": self.train_1_direction,
                },
                {
                    "train": self.train_2,
                    "train_time": self.train_2_time,
                    "train_direction": self.train_2_direction,
                },
                {
                    "train": self.train_3,
                    "train_time": self.train_3_time,
                    "train_direction": self.train_3_direction,
                },
                {
                    "train": self.train_4,
                    "train_time": self.train_4_time,
                    "train_direction": self.train_4_direction,
                },
            ]
            try:
                common.all_data_to_json(
                    self.loading,
                    self.station,
                    self.next_four_trains,
                    self.all_train_data,
                )
                time.sleep(5)

            except Exception as e:
                note = f"Error saving all data to json: {str(e)}"
                common.log_add(note, "System", 2)

    def station_load(self):
        try:
            cycle_check = common.config_load_v2()[constants.CYCLE]
            self.force_change_station_check = common.config_load_v2()[
                constants.FORCE_CHANGE_STATION
            ]

            if self.force_change_station_check != "":
                self.station = self.force_change_station_check
                self.previous_station = self.force_change_station_check
                self.cycle_station = self.force_change_station_check
                self.train_loading()
                self.station_pos = 65
                note = "New Station: " + self.station
                common.log_add(note, "Display", 2)
                all_configs = common.config_load_v2()
                all_configs[constants.FORCE_CHANGE_STATION] = ""
                common.update_json(constants.CONFIG_FILE, all_configs)

            else:
                if cycle_check is True:
                    new_station = self.cycle_station
                    station_check = common.station_check_v2(new_station)
                else:
                    new_station = common.config_load_v2()[constants.STATION]
                    station_check = common.station_check_v2(new_station)

                if station_check is True:
                    if new_station != self.previous_station:
                        self.station = new_station
                        self.previous_station = new_station
                        self.train_loading()
                        self.station_pos = 65
                        note = "New Station: " + self.station
                        common.log_add(note, "Display", 2)
                    else:
                        self.station = new_station
                        note = "No Station Change"
                        common.log_add(note, "Display", 4)

                else:
                    self.station_load_error = True
                    note = (
                        "ERROR: Station check result false, check spelling. Station in config: "
                        + new_station
                    )
                    common.log_add(note, "Display", 1)

        except Exception as e:
            note = f"ERROR: Station load: {str(e)}"
            common.log_add(note, "Display", 1)

    def subway_line_print(self, lines):
        line_draw = draw()
        circle_location = 66
        text_location = 69
        for x in lines:
            circle_color = self.train_colors(x)
            if len(x) == 1:
                line_draw.local_train(self.canvas, circle_location, 20, circle_color)
                graphics.DrawText(
                    self.canvas, self.font, text_location, 27, self.in_circle_color, x
                )
                circle_location += 10
                text_location += 10
            else:
                x = x[0]
                line_draw.express_train(self.canvas, circle_location, 20, circle_color)
                graphics.DrawText(
                    self.canvas, self.font, text_location, 27, self.in_circle_color, x
                )
                circle_location += 10
                text_location += 10

    def train_colors(self, train):
        if train in ["A", "C", "E", "H"]:
            return graphics.Color(0, 57, 166)
        elif train in ["B", "D", "F", "FX", "M"]:
            return graphics.Color(255, 99, 25)
        elif train in ["G", "GS"]:
            return graphics.Color(108, 190, 69)
        elif train in ["J", "Z"]:
            return graphics.Color(153, 102, 51)
        elif train in ["L"]:
            return graphics.Color(167, 169, 172)
        elif train in ["N", "Q", "R", "W"]:
            return graphics.Color(252, 204, 10)
        elif train in ["S", "FS", "L"]:
            return graphics.Color(128, 129, 131)
        elif train in ["1", "2", "3"]:
            return graphics.Color(238, 53, 46)
        elif train in ["4", "5", "6", "6X"]:
            return graphics.Color(0, 147, 60)
        elif train in ["7", "7X"]:
            return graphics.Color(185, 51, 173)
        elif train in ["T"]:
            return graphics.Color(0, 173, 208)
        elif train in ["!"]:
            return graphics.Color(255, 0, 0)
        elif train in ["SI"]:
            return graphics.Color(149, 153, 160)

        elif train == "":
            return graphics.Color(0, 0, 0)
        else:
            note = train + "Color load error"
            common.log_add(note, "Display", 1)
            return graphics.Color(0, 0, 0)

    def train_display(self, train, train_time, direction, top):
        line_draw = draw()
        if top is True:
            add_number = self.add_number_1
            height = 17
        elif top is False:
            add_number = self.add_number_2
            height = 27
        time = str(train_time) + "min"
        circle_color = self.train_colors(train)
        text_color = self.waiting_color
        if len(train) == 1:
            local = True
        else:
            local = False
        if self.loading is True:
            pass
        else:
            if local is True:
                if top is True:
                    line_draw.local_train(self.canvas, 64, 10, circle_color)
                    graphics.DrawText(
                        self.canvas, self.font, 67, height, self.in_circle_color, train
                    )
                if top is False:
                    line_draw.local_train(self.canvas, 64, 20, circle_color)
                    graphics.DrawText(
                        self.canvas, self.font, 67, height, self.in_circle_color, train
                    )
            if local is False:
                if top is True:
                    line_draw.express_train(self.canvas, 64, 10, circle_color)
                    graphics.DrawText(
                        self.canvas, self.font, 67, height, self.in_circle_color, train
                    )
                if top is False:
                    line_draw.express_train(self.canvas, 64, 20, circle_color)
                    graphics.DrawText(
                        self.canvas, self.font, 67, height, self.in_circle_color, train
                    )
        if train_time == 0:
            text_color = self.arrival_color
        elif len(time) == 4:
            graphics.DrawText(self.canvas, self.font, 112, height, text_color, time)
            text_color = self.waiting_color
        elif len(time) == 5:
            graphics.DrawText(self.canvas, self.font, 109, height, text_color, time)
        if train_time == 0 or train_time == "":
            if len(direction) > 13:
                start_number = 0
                end_number = 13
                if (end_number + add_number) < (len(direction) + 13):
                    print_text = direction[
                        (start_number + add_number) : (end_number + add_number)
                    ]
                    graphics.DrawText(
                        self.canvas, self.font, 74, height, text_color, print_text
                    )
                    if top is True:
                        self.add_number_1 += 1
                    if top is False:
                        self.add_number_2 += 1
                else:
                    print_text = direction[
                        (start_number + add_number) : (end_number + add_number)
                    ]
                    graphics.DrawText(
                        self.canvas, self.font, 74, height, text_color, print_text
                    )
                    if top is True:
                        self.add_number_1 = 0
                    if top is False:
                        self.add_number_2 = 0
            else:
                graphics.DrawText(
                    self.canvas, self.font, 74, height, text_color, direction
                )
        else:
            if len(direction) > 8:
                if train_time == 0:
                    start_number = 0
                    end_number = 13
                    if (end_number + add_number) < (len(direction) + 13):
                        print_text = direction[
                            (start_number + add_number) : (end_number + add_number)
                        ]
                        graphics.DrawText(
                            self.canvas, self.font, 74, height, text_color, print_text
                        )
                        if top is True:
                            self.add_number_1 += 1
                        if top is False:
                            self.add_number_2 += 1
                    else:
                        print_text = direction[
                            (start_number + add_number) : (end_number + add_number)
                        ]
                        graphics.DrawText(
                            self.canvas, self.font, 74, height, text_color, print_text
                        )
                        if top is True:
                            self.add_number_1 = 0
                        if top is False:
                            self.add_number_2 = 0
                else:
                    start_number = 0
                    end_number = 8
                    if (end_number + add_number) < (len(direction) + 8):
                        print_text = direction[
                            (start_number + add_number) : (end_number + add_number)
                        ]
                        graphics.DrawText(
                            self.canvas, self.font, 74, height, text_color, print_text
                        )
                        if top is True:
                            self.add_number_1 += 1
                        if top is False:
                            self.add_number_2 += 1
                    else:
                        print_text = direction[
                            (start_number + add_number) : (end_number + add_number)
                        ]
                        graphics.DrawText(
                            self.canvas, self.font, 74, height, text_color, print_text
                        )
                        if top is True:
                            self.add_number_1 = 0
                        if top is False:
                            self.add_number_2 = 0
            else:
                graphics.DrawText(
                    self.canvas, self.font, 74, height, text_color, direction
                )

    def train_loading(self):
        self.train_1 = ""
        self.train_1_time = ""
        self.train_1_direction = "Loading..."
        self.train_2 = ""
        self.train_2_time = ""
        self.train_2_direction = ""
        self.train_3 = ""
        self.train_3_time = ""
        self.train_3_direction = "Loading..."
        self.train_4 = ""
        self.train_4_time = ""
        self.train_4_direction = ""
        self.add_number_1 = 0
        self.add_number_2 = 0
        self.add_number_3 = 0
        self.add_number_4 = 0
        self.all_train_data = {}
        self.next_four_trains = {}
        self.loading = True
        self.station = common.config_load_v2()["station"]
        note = "Train Info Loading"
        common.log_add(note, "Display", 4)


if __name__ == "__main__":
    sub = nyc_subway()
    sub.run()
