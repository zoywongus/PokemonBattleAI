from gym.envs.registration import register

register(
    id='Pokemon',
    entry_point='gym_game.envs:PokEnv',
    max_episode_steps=2000,
)