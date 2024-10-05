import numpy as np
import pytensor.tensor as pt

def flatten_samples(samples):
    """
    Flatten MCMC samples from shape (chains, draws, ...) to (n_samples, ...).

    Parameters:
    - samples (np.ndarray): The array of samples to flatten.

    Returns:
    - np.ndarray: Flattened samples.
    """
    sample_dims = samples.shape
    num_dims = len(sample_dims)

    # If samples have more than two dimensions (e.g., chains, draws, parameter_dims)
    if num_dims > 2:
        chains, draws = samples.shape[0], samples.shape[1]
        param_shape = samples.shape[2:]
        new_shape = (chains * draws,) + param_shape
        return samples.reshape(new_shape)
    else:
        # Samples have shape (chains, draws)
        return samples.reshape(-1)

class SuperLigaPredictor:
    def __init__(self, trace, teams):
        """
        Initialize the predictor with the MCMC trace and list of teams.

        Parameters:
        - trace: The MCMC trace containing posterior samples.
        - teams (list): List of team names.
        """
        self.trace = trace
        self.teams = teams
        self.team_encoder = {team: idx for idx, team in enumerate(teams)}
        self._prepare_samples()

    def _prepare_samples(self):
        """
        Extract and flatten parameter samples from the trace.
        """
        # Extract parameter samples and flatten them
        self.home_advantage_samples = flatten_samples(
            self.trace.posterior['home_advantage'].values
        )
        self.attack_strength_samples = flatten_samples(
            self.trace.posterior['attack_strength'].values
        )
        self.defense_strength_samples = flatten_samples(
            self.trace.posterior['defense_strength'].values
        )

    def predict_match(self, home_team, away_team, num_simulations=None):
        """
        Predict the outcome of a match between two teams.

        Parameters:
        - home_team (str): Name of the home team.
        - away_team (str): Name of the away team.
        - num_simulations (int or None): Number of simulations to run (default: None).
                                         If None, use all available samples.

        Returns:
        - dict: A dictionary containing predicted probabilities and expected goals.
        """
        # Map team names to indices
        home_team_idx = self.team_encoder.get(home_team)
        away_team_idx = self.team_encoder.get(away_team)

        if home_team_idx is None or away_team_idx is None:
            raise ValueError("Team names not found in the team list.")

        # Extract samples for the specific teams
        home_attack_strength = self.attack_strength_samples[:, home_team_idx]
        home_defense_strength = self.defense_strength_samples[:, home_team_idx]
        away_attack_strength = self.attack_strength_samples[:, away_team_idx]
        away_defense_strength = self.defense_strength_samples[:, away_team_idx]
        home_advantage = self.home_advantage_samples

        # Convert to PyTensor tensors
        home_advantage_pt = pt.as_tensor_variable(home_advantage)
        home_attack_strength_pt = pt.as_tensor_variable(home_attack_strength)
        home_defense_strength_pt = pt.as_tensor_variable(home_defense_strength)
        away_attack_strength_pt = pt.as_tensor_variable(away_attack_strength)
        away_defense_strength_pt = pt.as_tensor_variable(away_defense_strength)

        # Compute expected goals using the model
        theta_home = pt.exp(
            home_advantage_pt +
            home_attack_strength_pt -
            away_defense_strength_pt
        )
        theta_away = pt.exp(
            away_attack_strength_pt -
            home_defense_strength_pt
        )

        # Evaluate tensors to get numerical values
        theta_home_val = theta_home.eval()
        theta_away_val = theta_away.eval()

        # If num_simulations is specified, sample indices
        if num_simulations is not None:
            total_samples = len(theta_home_val)
            if num_simulations > total_samples:
                raise ValueError(f"num_simulations ({num_simulations}) cannot be greater than the number of available samples ({total_samples}).")
            indices = np.random.choice(total_samples, size=num_simulations, replace=False)
            theta_home_val = theta_home_val[indices]
            theta_away_val = theta_away_val[indices]

        # Simulate goals based on expected goals
        simulated_home_goals = np.random.poisson(theta_home_val)
        simulated_away_goals = np.random.poisson(theta_away_val)

        # Calculate probabilities of different outcomes
        prob_home_win = np.mean(simulated_home_goals > simulated_away_goals)
        prob_draw = np.mean(simulated_home_goals == simulated_away_goals)
        prob_away_win = np.mean(simulated_home_goals < simulated_away_goals)

        # Calculate expected goals
        expected_home_goals = np.mean(theta_home_val)
        expected_away_goals = np.mean(theta_away_val)

        return {
            'home_team': home_team,
            'away_team': away_team,
            'probabilities': {
                'home_win': prob_home_win,
                'draw': prob_draw,
                'away_win': prob_away_win
            },
            'expected_goals': {
                home_team: expected_home_goals,
                away_team: expected_away_goals
            }
        }

    def print_prediction(self, prediction):
        """
        Print the prediction results in a readable format.

        Parameters:
        - prediction (dict): The dictionary returned by predict_match.
        """
        home_team = prediction['home_team']
        away_team = prediction['away_team']
        probs = prediction['probabilities']
        expected_goals = prediction['expected_goals']

        print(f"Predicted probabilities for {home_team} vs {away_team}:")
        print(f"Home win probability: {probs['home_win']:.2%}")
        print(f"Draw probability: {probs['draw']:.2%}")
        print(f"Away win probability: {probs['away_win']:.2%}")
        print(f"\nExpected goals:")
        print(f"{home_team}: {expected_goals[home_team]:.2f}")
        print(f"{away_team}: {expected_goals[away_team]:.2f}")
