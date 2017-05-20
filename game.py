from random import shuffle
supplies = {'clay':0, 'veggies':1, 'grain':2, 'wood':3, 'stone':4, 'reed':5, 'sheeps':6, 'pigs':7, 'cows':8, 'food':9}

class Game():
    def __init__(self):
        self.board = Board()
        self.playerList = [Mat('e'), Mat('c'), Mat('r')]
        self.numRounds = 14
        self.stages = [0,0,0,0,1,1,1,2,2,3,3,4,4,5]
        self.harvests = [3,6,8,10,12,13] #rounds after which there are harvests, 0-indexed
        self.startingPlayer = 0
        self.adultPortion = 2
        self.babyPortion = 1


    def play(self):
        for round in range(self.numRounds):
            self.executeRound(round)
            if round in self.harvests:
                self.executeHarvest()


    def executeRound(self, round):
        currentStage = self.stages[round]
        print("stage:{}\nround:{}\n".format(currentStage+1,round+1))

        #reveal new action card
        self.board.revealAction()

        #add to all piles
        for action in self.board.actions:
            if isinstance(action,Pile):
                action.refill()


        #players take turns choosing cards
        #make a list of the starting player and then the others
        order = self.playerList[self.startingPlayer:] + self.playerList[:self.startingPlayer]
        #print(max(lambda x: self.playerList[x].members, list(range(len(self.playerList)))))

        numActions = max(self.playerList, key=lambda p: p.members).members
        chosenActions = []

        for i in range(numActions):
            #print current board
            print(self.board)
            print("already chosen: " + str(chosenActions))

            for player in self.playerList:
                if player.members > i:
                    #get the player input
                    while True:
                        print(player)
                        raw_choice = input("player {}! pick an action, any action! (enter 'q' quit being so loopy): ".format(player.name))
                        if raw_choice == "q":
                           quit()
                        try:
                            choice = int(raw_choice)
                        except ValueError:
                            continue
                        else:
                            if choice in chosenActions:
                                print("already chosen, try again")
                            elif choice < 1 or choice > len(self.board.actions):
                                print("not an option, try again")
                            else:
                                break

                    self.board.actions[choice-1].execute(player)
                    chosenActions.append(choice)


    def executeHarvest(self):

        for player in self.playerList:

        #harvest fields #TODO implement

        #feed family
            player.stores[supplies['food']] -= player.babies * self.babyPortion + player.members * self.adultPortion
            if player.stores[supplies['food']] > 0:
                player.beggingCards += (player.stores[supplies['food']] * -1)
                player.stores[supplies['food']] = 0

        #babies grow
            player.members += player.babies
            player.babies = 0

        #breeding #TODO test!
            for animal in [supplies['sheeps'],supplies['pigs'],supplies['cows']]:
                if player.stores[animal] >= 2:
                    player.stores[animal] += 1





class Board():
    def __init__(self):
        #[pile 3 wood, pile 1 clay, pile 1 reed, pile 1 food]
        startingActions = [Pile(3,"wood"),Pile(1,"clay"),Pile(1,"reed"),Pile(1,"food")]
        #[building and/or stables, start player and/or minor improve, take 1 grain, mat field, card occupation, take 2 food]
        twoPlayerActions = [Build("room"),StartingPlayer(),Take(1,"grain"),Build("field"),Card("occupation"),Take(2,"food")]
        #there will be more sets of starting actions with number of players
        self.actions = startingActions + twoPlayerActions #TODO do this in a player dependent way
        roundActions = [[Pile(1,"sheeps"),Sow(),Card("improvement"),Build("fences")],[Renovate(),Pile(1,"Stone"),FamilyGrow()],[Pile(1,"pigs"),Take(1,"veggies")],[Pile(1,"cows"),Pile(1,"stone")],[Sow(),FamilyGrow()],[Build("Fences")]]
        #TODO i guess these have some upper case to make them unique??? terrible idea
        self.roundActions = []
        for stack in roundActions:
            shuffle(stack)
            self.roundActions = self.roundActions + stack

    def revealAction(self):
        self.actions.append(self.roundActions.pop(0))

    def __str__(self):
        output = ""
        for i in range(len(self.actions)):
            output += "{}: {}\n".format(i+1,str(self.actions[i]))
        return output

class Mat():
    def __init__(self,name):
        self.name = name
        self.grid = [[None,None,None,None,None],["WH",None,None,None,None],["WH",None,None,None,None]]
        self.stores = [0,0,0,0,0,0,0,0,0,0] #dict encodes what these are
        self.playedCards = []
        self.members = 2
        self.babies = 0
        self.beggingCards = 0

    def __str__(self):
        output = "{}'s mat:\n{} members\n\n".format(self.name, self.members)
        #print stores
        for i in range(len(self.stores)):
            output += "{}: {}\n".format(dict((v, k) for k, v in supplies.items())[i], self.stores[i])
        #print grid
        for r in self.grid:
            output += "\n"
            for c in r:
                output += "{}\t".format(c)
        return output


class Space():
    pass

class House(Space):
    pass

class Field(Space):
    pass

class Pasture(Space):
    pass



class Action():
    pass

class Pile(Action):
    def __init__(self, fill, thing):
        self.thing = thing
        self.held = 0
        self.fill = fill

    def refill(self):
        self.held = self.held + self.fill

    def execute(self, mat):
        mat.stores[supplies[self.thing]] += self.held
        self.held = 0

    def __str__(self):
        return "pile of {} {} (+{})".format(self.held, self.thing, self.fill)

class Take(Action):
    def __init__(self, amount, thing):
        self.thing = thing
        self.amount = amount

    def execute(self,mat):
        mat.stores[supplies[self.thing]] += self.amount

    def __str__(self):
        return "take {} {}".format(self.amount, self.thing)

class Build(Action):
    def __init__(self, kind):
        self.kind = kind

    def execute(self,mat):
        #TODO choose r and c
        r = 1
        c = 1
        mat.grid[r][c] = self.kind

    def __str__(self):
        return "build {}".format(self.kind)

class Card(Action):
    def __init__(self, kind):
        self.kind = kind

    def execute(self,mat):
        mat.playedCards.append(self.kind)

    def __str__(self):
        return self.kind

class StartingPlayer(Action):
    def execute(self, mat):
        pass

    def __str__(self):
        return "starting player"

class FamilyGrow(Action):
    def execute(self, mat):
        pass

    def __str__(self):
        return "family growth"

class Sow(Action):
    def execute(self, mat):
        pass

    def __str__(self):
        return "sow"

class Renovate(Action):
    def execute(self, mat):
        pass

    def __str__(self):
        return "renovate"
