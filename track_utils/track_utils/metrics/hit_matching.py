__author__ = 'Mikhail Hushchyn'

import numpy


class HitsMatchingEfficiencyLabels(object):

    def __init__(self, eff_threshold=0.5, min_hits_per_track=2):
        """
        This class calculates track efficiencies, reconstruction efficiency, ghost rate and clone rate
        for one event using hits matching approach.

        Parameters
        ----------
        eff_threshold : float
            Threshold value of a track efficiency to consider the track as a reconstructed one.
        min_hits_per_track : int
            Minimum number of hit per one recognized track.
        """

        self.eff_threshold = eff_threshold
        self.min_hits_per_track = min_hits_per_track

    def fit(self, true_labels, reco_labels):
        """
        The method calculates the metrics.

        Parameters
        ----------
        true_labels : array-like
            True hit labels.
        reco_labels : array-like
            Recognized hit labels.
        """

        true_labels = numpy.array(true_labels)
        reco_labels = numpy.array(reco_labels)


        unique_labels = numpy.unique(reco_labels)

        # Calculate efficiencies
        efficiencies = []
        tracks_id = []

        for label in unique_labels:
            if label != -1:

                track = true_labels[reco_labels == label]
                unique, counts = numpy.unique(track, return_counts=True)

                if len(track) >= self.min_hits_per_track:

                    eff = 1. * counts.max() / len(track)
                    efficiencies.append(eff)
                    tracks_id.append(unique[counts == counts.max()][0])

        tracks_id = numpy.array(tracks_id)
        efficiencies = numpy.array(efficiencies)
        self.efficiencies_ = efficiencies

        # Calculate avg. efficiency
        avg_efficiency = efficiencies.mean()
        self.avg_efficiency_ = avg_efficiency

        # Calculate reconstruction efficiency
        true_tracks_id = numpy.unique(true_labels)
        n_tracks = (true_tracks_id != -1).sum()

        reco_tracks_id = tracks_id[efficiencies >= self.eff_threshold]
        unique, counts = numpy.unique(reco_tracks_id[reco_tracks_id != -1], return_counts=True)

        if n_tracks > 0:
            reconstruction_efficiency = 1. * len(unique) / (n_tracks)
            self.reconstruction_efficiency_ = reconstruction_efficiency
        else:
            self.reconstruction_efficiency_ = 0

        # Calculate ghost rate
        if n_tracks > 0:
            ghost_rate = 1. * (len(tracks_id) - len(reco_tracks_id[reco_tracks_id != -1])) / (n_tracks)
            self.ghost_rate_ = ghost_rate
        else:
            self.ghost_rate_ = 0

        # Calculate clone rate
        reco_tracks_id = tracks_id[efficiencies >= self.eff_threshold]
        unique, counts = numpy.unique(reco_tracks_id[reco_tracks_id != -1], return_counts=True)

        if n_tracks > 0:
            clone_rate = (counts - numpy.ones(len(counts))).sum() / (n_tracks)
            self.clone_rate_ = clone_rate
        else:
            self.clone_rate_ = 0




class HitsMatchingEfficiencyIndeces(object):

    def __init__(self, eff_threshold=0.5, min_hits_per_track=2):
        """
        This class calculates track efficiencies, reconstruction efficiency, ghost rate and clone rate
        for one event using hits matching approach.

        Parameters
        ----------
        eff_threshold : float
            Threshold value of a track efficiency to consider the track as a reconstructed one.
        min_hits_per_track : int
            Minimum number of hit per one recognized track.
        """

        self.eff_threshold = eff_threshold
        self.min_hits_per_track = min_hits_per_track

    def fit(self, true_labels, track_inds):
        """
        The method calculates all metrics.

        Parameters
        ----------
        true_labels : array-like
            True labels of hits.
        track_inds : array-like
            Hit indeces of recognized tracks.
        """

        track_efficiencies = []
        track_labels = []
        reco_eff = 0
        n_ghosts = 0

        n_tracks = len(numpy.unique(true_labels))

        for one_track in track_inds:

            one_track = numpy.unique(one_track)

            if len(one_track) < self.min_hits_per_track:
                one_track_eff = 0
                track_efficiencies.append(one_track_eff)
                continue

            hits_labels = true_labels[one_track]
            unique_hits_labels, count_hits_labels = numpy.unique(hits_labels, return_counts=True)
            one_track_eff = 1. * count_hits_labels.max() / len(one_track)
            one_track_label = unique_hits_labels[count_hits_labels == count_hits_labels.max()]

            track_efficiencies.append(one_track_eff)

            if one_track_eff >= self.eff_threshold:
                track_labels.append(one_track_label)
            else:
                n_ghosts += 1


        self.efficiencies_ = track_efficiencies
        if len(track_efficiencies) == 0:
            self.avg_efficiency_ = 0
        else:
            self.avg_efficiency_ = numpy.array(track_efficiencies).mean()


        if n_tracks == 0:
            self.ghost_rate_ = 0
        else:
            self.ghost_rate_ = 1. * n_ghosts / n_tracks


        if n_tracks == 0 or len(track_labels) == 0:
            self.reconstruction_efficiency_ = 0
        else:
            self.reconstruction_efficiency_ = 1. * len(numpy.unique(track_labels)) / n_tracks


        if n_tracks == 0 or len(track_labels) == 0:
            self.clone_rate_ = 0
        else:
            self.clone_rate_ = 1. * (len(track_labels) - len(numpy.unique(track_labels))) / n_tracks

