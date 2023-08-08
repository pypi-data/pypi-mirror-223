import os
from itertools import chain

import numpy as np
from markovclick.models import MarkovClickstream
import pygraphviz as pgv
from collections import Counter

from pypdf import PdfWriter, PdfReader

from sklearn.linear_model import LinearRegression

import datetime

class MarkovChainsWC(MarkovClickstream):

    def __init__(self, clickstream_list: list = None, prefixed: bool = True, time_cilckstream: list = None,
                 reg_srok_clickstream: list = None) -> object:

        self.clickstream_list = clickstream_list
        self.prefixed = prefixed

        self.time_cilckstream = time_cilckstream
        self.reg_srok_clickstream = reg_srok_clickstream
        self.koef_list = []

        self.pages = []
        super().get_unique_pages(prefixed=prefixed)

        self._count_matrix = None
        super().initialise_count_matrix()
        self._prob_matrix = None

        self.populate_count_matrix()
        super().compute_prob_matrix()

        self.label_node_dict = None
        self.get_label_node()

        self.transition_time_predictions = dict()
        self.__get_transition_time_predictions()

    def __get_transition_time_predictions(self):
        flattened_clickstream = list(chain.from_iterable(self.clickstream_list))
        time_data = np.array([(self.time_cilckstream[i + 1] - self.time_cilckstream[i]).total_seconds() / 3600
                              for i in range(len(flattened_clickstream) - 1)])
        X = np.array([[self.pages.index(flattened_clickstream[i]), self.pages.index(flattened_clickstream[i + 1])]
                      for i in range(len(flattened_clickstream) - 1)])
        y = time_data.reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        for i, page_i in enumerate(self.pages):
            for j, page_j in enumerate(self.pages):
                if self.prob_matrix[i,j] == 0:
                    self.transition_time_predictions[(page_i,page_j)] = None
                else:
                    state_pair = np.array([[self.pages.index(page_i), self.pages.index(page_j)]])
                    predicted_hours = max(0, model.predict(state_pair)[0])
                    total_seconds = int(predicted_hours * 3600)
                    time_delta_str = str(datetime.timedelta(seconds=total_seconds))
                    self.transition_time_predictions[(page_i, page_j)] = time_delta_str

    @property
    def count_matrix(self):
        """
        Sets attribute to access the count matrix
        """
        return self._count_matrix

    @property
    def prob_matrix(self):
        """
        Sets attribute to access the probability matrix
        """
        return self._prob_matrix

    def initialize_koef_list(self):
        flattened_clickstream = list(chain.from_iterable(self.clickstream_list))
        self.koef_list = np.ones(len(flattened_clickstream))

    def update_koef(self):

        self.initialize_koef_list()

        flattened_clickstream = list(chain.from_iterable(self.clickstream_list))

        for el in self.get_unique_pages():
            indexes = [i for i,j in enumerate(flattened_clickstream) if j == el]

            temp_koef_list = np.ones(len(indexes))

            for i in range(1,len(indexes)):
                reglament_hours = self.reg_srok_clickstream[indexes[i]]
                n_hours = (self.time_cilckstream[indexes[i]] - self.time_cilckstream[indexes[i-1]]).total_seconds() / 3600
                if n_hours < reglament_hours:
                    temp_koef_list[i] = (1/reglament_hours)*n_hours
                self.koef_list[indexes[i]] = temp_koef_list[i]

    def populate_count_matrix(self):
        """
        Assembles a matrix of counts of transitions from each possible state,
        to every other possible state.
        """

        self.initialise_count_matrix()
        self.update_koef()
        # For each session in list of sessions
        for session in self.clickstream_list:
            for j in range(0, len(session) - 1):
                next_state = self.pages.index(session[j+1])
                current_state = self.pages.index(session[j])
                self._count_matrix[current_state, next_state] += 1*self.koef_list[j+1]

        return self._count_matrix

    def get_label_node(self):
        flattened_clickstream = list(chain.from_iterable(self.clickstream_list))
        self.label_node_dict = Counter(flattened_clickstream)

    def draw_node(self,least_percent : float = 0, graph_label : str = '', filename : str = 'result'):
        G = pgv.AGraph(directed=True)

        for state in self.pages:
            for transition in self.pages:
                rate = self.prob_matrix[self.pages.index(state),self.pages.index(transition)]
                if rate >= least_percent:
                    transition_time = self.transition_time_predictions.get((state, transition), "N/A")
                    if rate < 0.25:
                        G.add_edge(state, transition,
                                   label=f"prob = {round(rate, 2)}\ntime = {transition_time}", color='#93d42a',fontsize=8)
                    elif rate < 0.5:
                        G.add_edge(state, transition,
                                   label=f"prob = {round(rate, 2)}\ntime = {transition_time}", color='#2aafd4',fontsize=8)
                    elif rate < 0.75:
                        G.add_edge(state, transition,
                                   label=f"prob = {round(rate, 2)}\ntime = {transition_time}", color='#d4a62a',fontsize=8)
                    elif rate > 0.75:
                        G.add_edge(state, transition,
                                   label=f"prob = {round(rate, 2)}\ntime = {transition_time}", color='#d42a2a',fontsize=8)

        for key,value in self.label_node_dict.items():
            try:
                n = G.get_node(key)
                n.attr['label'] = f'{key} ({value})'
            except:
                pass
        G.graph_attr["label"] = graph_label
        G.draw('temp.pdf', prog='dot', format='pdf')

        writer = PdfWriter()

        reader_pdf = PdfReader('temp.pdf')

        try:
            reader_output = PdfReader(f'{filename}.pdf')
            for page in reader_output.pages:
                writer.add_page(page)
        except:
            pass

        for page in reader_pdf.pages:
            writer.add_page(page)

        writer.write(f'{filename}.pdf')
        writer.close()

        os.remove('temp.pdf')