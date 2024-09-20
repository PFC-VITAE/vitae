class CandidateFilter:

    def apply_filters(self, candidates, mission):
        mission_ranks = [rank.strip() for rank in mission.rank.split(',')]
        mission_profiles = [profile.strip().lower() for profile in mission.profile.split(',')]
        mission_degree_type = self.get_degree_type(mission.code)

        filtered_candidates = []
        for candidate in candidates:
            if self.filter_rank(mission_ranks, candidate) and self.filter_profile(mission_profiles, candidate) and self.filter_degree(mission_degree_type, candidate):
                filtered_candidates.append(candidate)
        return filtered_candidates
    
    def filter_rank(self, mission_ranks, candidate):
        return candidate.rank in mission_ranks
    
    def get_degree_type(self, mission_code):
        if 'D' in mission_code:
            return 'Doctorate'
        elif 'M' in mission_code:
            return 'Master'
        return 'Undefined'

    def filter_profile(self, mission_profiles, candidate):
        candidate_profile = candidate.qas_qms.strip().lower()
        if any(profile.startswith("qualquer") for profile in mission_profiles):
            return True
        else:
            if "qem/compt ou q/a/sv aman" in mission_profiles:
                special_profiles = ["qem compt", "cav", "inf", "art", "eng", "com", "sv int"]
                return candidate_profile in special_profiles
            return candidate_profile in mission_profiles
        
    def filter_degree(self, mission_degree_type, candidate):
        if mission_degree_type == "Master":
            if hasattr(candidate, "master") and candidate.master:
                return False
        elif mission_degree_type == "Doctorate":
            if hasattr(candidate, "master") and candidate.master:
                if hasattr(candidate, "doctorate") and not candidate.doctorate:
                    return True
                else:
                    return False
            else:
                return False
        return True
        
   