class CandidateFilter:

    def apply_filters(self, candidates, mission):
        mission_ranks = [rank.strip() for rank in mission["posto"].split(',')]
        mission_profiles = [profile.strip().lower() for profile in mission["perfil"].split(',')]

        filtered_candidates = []
        for candidate in candidates:
            if candidate.rank in mission_ranks and self.filter_profile(mission_profiles, candidate.qas_qms):
                filtered_candidates.append(candidate)
        return filtered_candidates

    def filter_profile(self, mission_profiles, candidate_profile):
        if any(profile.startswith("qualquer") for profile in mission_profiles):
            return True
        else:
            candidate_profile_lower = candidate_profile.strip().lower()
            if "qem/compt ou q/a/sv aman" in mission_profiles:
                special_profiles = ["qem compt", "cav", "inf", "art", "eng", "com", "sv int"]
                return candidate_profile_lower in special_profiles
            return candidate_profile_lower in mission_profiles
        
   