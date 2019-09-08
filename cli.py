#!/bin/python
import click


@click.group()
@click.option("-v", "--verbose", is_flag=True, default=False)
def cli():
    pass


@click.command()
@click.argument("path", type=click.Path(exists=True))
def prepros(path):
    from ops import SGF_folder_to_dataset
    # SGF_folder_rule_filter(sys.argv[1], "Chinese")
    SGF_folder_to_dataset(path)
    # SGF_file_to_dataset(sys.argv[1])


@click.command()
@click.option("-t", "--learn-type", type=click.Choice(["supervised", "reinforcement"]))
@click.option("--path-dataset", type=click.Path(exists=True))
def learn(learn_type, path_dataset):
    from GoNNAgent import GoNNAgent
    from libgoban import IGame
    import ops
    if learn_type == "supervised":
        # Supervised training
        board_size = 19
        go_agent = GoNNAgent(board_size)
        go_agent.supervised_training(path_dataset)
    else:
        # Reinforcement training
        board_size = 13
        go_agent = GoNNAgent(board_size)

        turn_max = int(board_size ** 2 * 2.)

        for i in range(1000):

            g = IGame(board_size)
            g.display_goban()

            total_turn = 0
            while not g.over():
                print("game {} - total_turn = {}".format(i, total_turn))

                move = go_agent.get_move(g)
                t_move = ops.move_scalar_to_tuple(move, board_size)
                if t_move in g.legals():
                    print(t_move)
                    g.play(t_move)
                else:
                    print("play pass")
                    g.play(None)
                g.display_goban()
                total_turn += 1
                if total_turn > turn_max:
                    break

            if total_turn > turn_max:
                winner = 2  # draw
                print("(Draw due to maximum moves)")
            else:
                score = g.outcome()
                print(score)
                winner = 2 if score[0] == score[1] else 0 if score[0] > score[1] else 1
            go_agent.end_game(winner)
    pass


cli.add_command(prepros)
cli.add_command(learn)

if __name__ == "__main__":
    cli()
