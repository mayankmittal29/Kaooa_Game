import pygame
import sys

pygame.init()
class KaooaGame:
  def __init__(self):
        self.killed_crows = 0
        self.vulture_x = 0
        self.vulture_y = 0
        self.all_coordinates = [[435, 66], [530, 346], [828, 350], [589, 527], [674, 808], [433, 640], [192, 807], [281, 526],[41, 350], [336, 352]]
        self.initial_positions = [[784,589],[735,646],[787,644],[840,644],[736,695],[791,697],[839,697],[102,644]] # of pennies
        self.list_of_adjacent_pairs=[[[435,66],[530,346]],[[530,346],[828,350]],[[828,350],[589,527]],[[589,527],[674,808]],[[674,808],[433,640]],[[433,640],[192,807]],[[192,807],[281,526]],[[281,526],[41,350]],[[41,350],[336,352]],[[336,352],[435,66]],[[336,352],[530,346]],[[530,346],[589,527]],[[589,527],[433,640]],[[433,640],[281,526]],[[281,526],[336,352]]]
        self.penny_having = [0,0,0,0,0,0,0,0,0,0]
        self.killing_pairs = [[[435,66],[10],[281,526]],[[435,66],[2],[589,527]],[[828,350],[2],[336,352]],[[828,350],[4],[433,640]],[[674,808],[4],[530,346]],[[674,808],[6],[281,526]],[[192,807],[6],[589,527]],[[192,807],[8],[336,352]],[[41,350],[8],[433,640]],[[41,350],[10],[530,346]]]
        self.adjacent_points = [[[435,66],[336,352],[530,346],[281,526],[589,527]],[[530,346],[435,66],[336,352],[589,527],[828,350],[41,350],[674,808]],[[828,350],[530,346],[589,527],[433,640],[336,352]],[[589,527],[828,350],[530,346],[674,808],[433,640],[435,66],[192,807]],[[674,808],[589,527],[433,640],[530,346],[281,526]],[[433,640],[674,808],[589,527],[192,807],[281,526],[41,350],[828,350]],[[192,807],[433,640],[281,526],[589,527],[336,352]],[[281,526],[192,807],[433,640],[336,352],[41,350],[435,66],[674,808]],[[41,350],[281,526],[336,352],[530,346],[433,640]],[[336,352],[435,66],[530,346],[41,350],[281,526],[192,807],[828,350]]]
        # self.adjacent_points = [[[435,66],[336,352],[530,346]],[[530,346],[435,66],[336,352],[589,527],[828,350]],[[828,350],[530,346],[589,527]],[[589,527],[828,350],[530,346],[674,808],[433,640]],[[674,808],[589,527],[433,640]],[[433,640],[674,808],[589,527],[192,807],[281,526]],[[192,807],[433,640],[281,526]],[[281,526],[192,807],[433,640],[336,352],[41,350]],[[41,350],[281,526],[336,352]],[[336,352],[435,66],[530,346],[41,350],[281,526]]]
        self.penny_radius = 20
        self.penny_positions = self.initial_positions
        self.current_player = 'crow'
        self.running = True
        self.not_all = 0
        self.wrong_turn = 0
        self.x_befordrag = 0
        self.y_beforedrag = 0
        self.cord_already = []
        self.click_on_space = 0
        self.all_on_star = 0
        self.vulture_rakh_diya = 0
        self.number_of__yellowpenny_in_star = 0
        self.result = -1        # if crow side wins -> 0 otherwise 1

  def is_inside_circle(self,pos, center, radius):
      # Check if the given position is inside the circle
      return (pos[0] - center[0]) ** 2 + (pos[1] - center[1]) ** 2 <= radius ** 2
        
  def display_alert(self,message, duration):
      alert_text = font.render(message, True, (0,0,0))
      screen.blit(alert_text, (screen_width // 2 - alert_text.get_width() // 2, screen_height // 2 - alert_text.get_height() // 2))
      pygame.display.flip()  # Update the display to immediately show the message
      pygame.time.delay(duration * 1000)  # Delay for the specified duration in milliseconds

  def display_alert_win(self,message, duration):
      alert_text = font.render(message, True, (0,0,0))
      screen.blit(alert_text, (screen_width // 2 - alert_text.get_width() // 2, screen_height // 2 - alert_text.get_height() // 2+80))
      pygame.display.flip()  # Update the display to immediately show the message
      pygame.time.delay(duration * 1000)  # Delay for the specified duration in milliseconds

  def delete_penny(self,index,all_coordinates,penny_positions):
      location_x = all_coordinates[index-1][0]
      location_y = all_coordinates[index-1][1]
      ans = -1
      for k, pos in enumerate(penny_positions):
        if(self.is_inside_circle((location_x,location_y),pos,self.penny_radius)):
          ans = k
          break
      penny_positions[ans][0]=1500
      penny_positions[ans][1]=1500

  def check_for_blockade_of_vulture(self,penny_positions,all_coordinates,adjacent_points,penny_having):
      location_x = penny_positions[7][0]
      location_y = penny_positions[7][1]
      coordidx = -1
      coordinate = []
      for k ,pos in enumerate(all_coordinates):
        if(self.is_inside_circle((location_x,location_y),pos,self.penny_radius)):
          coordidx = k
          coordinate = pos
          break
      flag = 1
      for l,adj in enumerate(adjacent_points):
        if(adj[0] == coordinate):
          for index,sath in enumerate(adj):
            if(index == 0):
              continue
            else:
              store = sath
              index = -1
              for b,pos in enumerate(all_coordinates):
               if(store == pos):
                index = b
                break
              if(penny_having[index]==0):
                flag = 0
                break
          if(flag == 0):
            break
      return flag

screen_width, screen_height = 860, 880
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kaooa Game!!")
image_path = "star.png"
image = pygame.image.load(image_path)
image_rect = image.get_rect()
clock = pygame.time.Clock()
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
font = pygame.font.SysFont(None, 100)

# Define dragging variables
dragging = False
dragging_index = None
offset_x = 0
offset_y = 0
font = pygame.font.SysFont(None, 36)
game_object = KaooaGame()
while game_object.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_object.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse click position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # x_befordrag=mouse_x
            # y_beforedrag=mouse_y
            idx = -1
            for i, pos in enumerate(game_object.penny_positions):
                if game_object.is_inside_circle((mouse_x,mouse_y),pos,game_object.penny_radius):
                   idx = i
                   break
            if(idx == -1):
              game_object.display_alert("Please click on some penny !",1)
              game_object.click_on_space = 1
            else:
                print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")
                game_object.x_befordrag=game_object.penny_positions[idx][0]
                game_object.y_beforedrag=game_object.penny_positions[idx][1]
                if(game_object.current_player == 'crow') and idx == 7:
                 game_object.display_alert("Crow's Turn !!",1)
                 game_object.wrong_turn = 1 
                elif(game_object.current_player == 'vulture')and idx !=7:
                 game_object.display_alert("Vulture's Turn !",1)
                 game_object.wrong_turn = 1
                for coord in game_object.all_coordinates:
                 if game_object.is_inside_circle((mouse_x,mouse_y),coord,20) and game_object.number_of__yellowpenny_in_star<7 and idx < 7 and game_object.current_player=='crow':
                    game_object.display_alert("First you have to add all crows !!",1)
                    game_object.cord_already=coord
                    game_object.not_all = 1
                    break
                # Check if the mouse click is inside any of the pennies
                for i, pos in enumerate(game_object.penny_positions):
                    if game_object.is_inside_circle((mouse_x, mouse_y), pos, game_object.penny_radius):
                        dragging = True
                        dragging_index = i
                        offset_x = pos[0] - mouse_x
                        offset_y = pos[1] - mouse_y
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
          dragging = False
            # Get the final position of the dragged penny
          if( game_object.click_on_space == 0):
            if( game_object.wrong_turn == 0):
                final_pos_x, final_pos_y = pygame.mouse.get_pos()
                # Check if the final position is close to any coordinate in all_coordinates
                if( game_object.is_inside_circle((final_pos_x,final_pos_y),(game_object.x_befordrag,game_object.y_beforedrag),20)):
                   game_object.display_alert("Kindly drag but not click on penny !",1)
                else:   
                    find = 0
                    if( game_object.not_all == 1):
                        game_object.not_all = 0
                        game_object.penny_positions[dragging_index][0]=game_object.cord_already[0]
                        game_object.penny_positions[dragging_index][1]=game_object.cord_already[1]
                    else:
                        if( game_object.all_on_star == 0):
                         if(dragging_index < 7):  # for yellow coins
                            for i,coord in enumerate(game_object.all_coordinates):
                                if game_object.is_inside_circle((final_pos_x, final_pos_y), coord, 20):
                                   if(game_object.penny_having[i] == 0):
                                    find = 1
                                    game_object.penny_having[i]=1
                                    if( game_object.number_of__yellowpenny_in_star<7):
                                      game_object.number_of__yellowpenny_in_star=game_object.number_of__yellowpenny_in_star+1
                                      if(game_object.number_of__yellowpenny_in_star == 7):
                                        game_object.all_on_star = 1
                                    break   
                            if(find == 1):
                             game_object.current_player = 'crow' if game_object.current_player == 'vulture' else 'vulture'
                            else:
                             game_object.penny_positions[dragging_index][0]=game_object.x_befordrag
                             game_object.penny_positions[dragging_index][1]=game_object.y_beforedrag
                             if(game_object.penny_having[i]==1):
                              game_object.display_alert("Kindly put the crow inside the empty circle !",1)
                             else:
                              game_object.display_alert("Kindly put the crow inside the circle !",1)
                            if(game_object.check_for_blockade_of_vulture(game_object.penny_positions,game_object.all_coordinates,game_object.adjacent_points,game_object.penny_having) and game_object.vulture_rakh_diya==1):
                              game_object.running = False
                              game_object.result = 0
                         else:  # for green coin
                          inix = game_object.x_befordrag
                          iniy = game_object.y_beforedrag
                          aftx = final_pos_x
                          afty = final_pos_y
                          coordinit = []
                          coordfinal = []
                          shuru = 0
                          baad = 0
                          mila = 0
                          final = 0  # finally suucessful 
                          if(game_object.vulture_rakh_diya == 0 ):   # first time putting vulture on board
                            for i,coord in enumerate(game_object.all_coordinates):
                                if game_object.is_inside_circle((final_pos_x, final_pos_y), coord, 20):
                                   if(game_object.penny_having[i] == 0):
                                    find = 1
                                    game_object.penny_having[i]=2
                                    break   
                            if(find == 1):
                             game_object.current_player = 'crow' if game_object.current_player == 'vulture' else 'vulture'
                             game_object.vulture_rakh_diya = 1
                            else:
                             game_object.penny_positions[dragging_index][0]=game_object.x_befordrag
                             game_object.penny_positions[dragging_index][1]=game_object.y_beforedrag
                             game_object.display_alert("Kindly put the vulture inside the circle !",1)
                          else:     # not the first time
                            for i,pos in enumerate(game_object.all_coordinates):
                             if game_object.is_inside_circle((inix,iniy),pos,20):
                                coordinit = pos
                                shuru = i
                                break
                            for j,pos in enumerate(game_object.all_coordinates):
                                if game_object.is_inside_circle((aftx,afty),pos,20):
                                 mila = 1
                                 coordfinal=pos
                                 baad =j
                                 break 

                            if(mila == 1):
                                index_kill = -1
                                kill = 0
                                list_of_possible_kills = []
                                # getting all possible killing scenarios
                                for k,pos in enumerate(game_object.killing_pairs):
                                 if(pos[0]==coordinit):
                                    middle = pos[1]
                                    index_kill = k
                                    ab=pos[2]
                                    destination_num = 0
                                    for i,cor in enumerate(game_object.all_coordinates):
                                     if(ab==cor):
                                        destination_num = i
                                        break
                                    if(game_object.penny_having[middle[0]-1]==1) and (game_object.penny_having[destination_num]==0):
                                      kill=kill+1
                                      list_of_possible_kills.append([coordinit,middle,ab])
                                 elif(pos[2]==coordinit):
                                     middle = pos[1]
                                     ab=pos[0]
                                     destination_num = 0
                                     for i,cor in enumerate(game_object.all_coordinates):
                                      if(ab==cor):
                                        destination_num = i
                                        break 
                                     if(game_object.penny_having[middle[0]-1]==1) and (game_object.penny_having[destination_num]==0):
                                      kill=kill+1
                                      list_of_possible_kills.append([coordinit,middle,ab])
                                if( kill == 0):
                                 if(([coordfinal,coordinit] in game_object.list_of_adjacent_pairs) or ([coordinit,coordfinal] in game_object.list_of_adjacent_pairs)) and game_object.penny_having[baad]==0:
                                  game_object.penny_having[shuru]=0
                                  game_object.penny_having[baad]=2
                                  game_object.current_player = 'crow' if game_object.current_player == 'vulture' else 'vulture'
                                 else:
                                  if(game_object.penny_having[baad]!=0):
                                    game_object.display_alert("You have placed on another penny !",1)
                                    game_object.penny_positions[dragging_index][0]=inix
                                    game_object.penny_positions[dragging_index][1]=iniy
                                  else:
                                    game_object.display_alert("You are allowed to move to only adjacent locations 1 !",1)
                                    game_object.penny_positions[dragging_index][0]=inix
                                    game_object.penny_positions[dragging_index][1]=iniy
                                else:
                                 marna = 0
                                 lineofmoth = []
                                 for k,mm in enumerate(list_of_possible_kills):
                                    if(mm[2]==coordfinal):
                                        marna = 1
                                        lineofmoth = mm
                                        break
                                 if(marna == 0):
                                    game_object.display_alert("U should have to kill the Crow !",1)
                                    game_object.penny_positions[dragging_index][0]=inix
                                    game_object.penny_positions[dragging_index][1]=iniy
                                 else:
                                    game_object.display_alert("Ahnn a Crow killed !",1)
                                    game_object.penny_having[shuru] = 0
                                    game_object.penny_having[baad] = 2
                                    idx=lineofmoth[1]
                                    game_object.penny_having[idx[0]-1] = 0
                                    # print(penny_having)
                                    # print(idx[0])
                                    # penny_positions[idx[0]-1][0]=1500
                                    # penny_positions[idx[0]-1][1]=1500
                                    game_object.delete_penny(idx[0],game_object.all_coordinates,game_object.penny_positions)
                                    game_object.killed_crows=game_object.killed_crows+1
                                    list_of_possible_kills = []
                                    game_object.current_player = 'crow' if game_object.current_player == 'vulture' else 'vulture'
                            else:
                                game_object.penny_positions[dragging_index][0]=inix
                                game_object.penny_positions[dragging_index][1]=iniy
                                game_object.display_alert("Kindly put the penny inside the circle !",1)
                         if(game_object.killed_crows >= 4):
                            game_object.running = False     
                            game_object.result = 1
                            # display_alert_win("Hurray!  Vulture Won",4)
                            # when all yellow have been put on board    
                        else:
                         inix = game_object.x_befordrag
                         iniy = game_object.y_beforedrag
                         aftx = final_pos_x
                         afty = final_pos_y
                         coordinit = []
                         coordfinal = []
                         shuru = 0
                         baad = 0
                         mila = 0
                         final = 0  # finally suucessful 
                         for i,pos in enumerate(game_object.all_coordinates):
                          if game_object.is_inside_circle((inix,iniy),pos,20):
                            coordinit = pos
                            shuru = i
                            break
                         for j,pos in enumerate(game_object.all_coordinates):
                            if game_object.is_inside_circle((aftx,afty),pos,20):
                             mila = 1
                             coordfinal=pos
                             baad =j
                             break
                         if(dragging_index<7): # for yellow coins
                           if(mila == 1):
                            if(([coordfinal,coordinit] in game_object.list_of_adjacent_pairs) or ([coordinit,coordfinal] in game_object.list_of_adjacent_pairs)) and game_object.penny_having[baad]==0:
                             game_object.penny_having[shuru]=0
                             game_object.penny_having[baad]=1
                             game_object.current_player = 'crow' if game_object.current_player == 'vulture' else 'vulture'
                            else:
                             if(game_object.penny_having[baad]!=0):
                              game_object.display_alert("You have placed on another penny !",1)
                              game_object.penny_positions[dragging_index][0]=inix
                              game_object.penny_positions[dragging_index][1]=iniy
                             else:
                              game_object.display_alert("You are allowed to move to only adjacent locations !",1)
                              game_object.penny_positions[dragging_index][0]=inix
                              game_object.penny_positions[dragging_index][1]=iniy
                           else:
                            game_object.penny_positions[dragging_index][0]=inix
                            game_object.penny_positions[dragging_index][1]=iniy
                            game_object.display_alert("Kindly put the penny inside the circle !",1)
                           if(game_object.check_for_blockade_of_vulture(game_object.penny_positions,game_object.all_coordinates,game_object.adjacent_points,game_object.penny_having) and game_object.vulture_rakh_diya==1):
                              game_object.running = False
                              game_object.result = 0
                         else:  # for green coin
                          if(mila == 1):
                            middle = []
                            index_kill = -1
                            kill = 0
                            list_of_possible_kills = []
                            for k,pos in enumerate(game_object.killing_pairs):
                             if(pos[0]==coordinit):
                                middle = pos[1]
                                index_kill = k
                                ab=pos[2]
                                destination_num =0
                                for i,cor in enumerate(game_object.all_coordinates):
                                   if(ab==cor):
                                      destination_num=i
                                if(game_object.penny_having[middle[0]-1]==1) and (game_object.penny_having[destination_num]==0):
                                 kill=kill+1
                                 list_of_possible_kills.append([coordinit,middle,ab])
                             elif(pos[2]==coordinit):
                                middle = pos[1]
                                ab=pos[0]
                                destination_num = 0
                                for i,cor in enumerate(game_object.all_coordinates):
                                  if(ab==cor):
                                    destination_num = i
                                    break 
                                if(game_object.penny_having[middle[0]-1]==1) and (game_object.penny_having[destination_num]==0):
                                  kill=kill+1
                                  list_of_possible_kills.append([coordinit,middle,ab])    
                            if( kill == 0):
                             if(([coordfinal,coordinit] in game_object.list_of_adjacent_pairs) or ([coordinit,coordfinal] in game_object.list_of_adjacent_pairs)) and game_object.penny_having[baad]==0:
                              game_object.penny_having[shuru]=0
                              game_object.penny_having[baad]=2
                              game_object.current_player = 'crow' if game_object.current_player == 'vulture' else 'vulture'
                             else:
                              if(game_object.penny_having[baad]!=0):
                                game_object.display_alert("You have placed on another penny !",1)
                                game_object.penny_positions[dragging_index][0]=inix
                                game_object.penny_positions[dragging_index][1]=iniy
                              else:
                                game_object.display_alert("You are allowed to move to only adjacent locations !",1)
                                game_object.penny_positions[dragging_index][0]=inix
                                game_object.penny_positions[dragging_index][1]=iniy
                            else:
                               marna = 0
                               lineofmoth = []
                               for k,mm in enumerate(list_of_possible_kills):
                                  if(mm[2]==coordfinal):
                                     marna = 1
                                     lineofmoth = mm
                                     break
                               if(marna == 0):
                                  game_object.display_alert("U should have to kill the Crow !",1)
                                  game_object.penny_positions[dragging_index][0]=inix
                                  game_object.penny_positions[dragging_index][1]=iniy
                               else:
                                  game_object.display_alert("Ahnn a Crow killed !",1)
                                  game_object.penny_having[shuru]=0
                                  game_object.penny_having[baad]=2
                                  idx=lineofmoth[1]
                                  game_object.penny_having[idx[0]-1] = 0
                                  game_object.delete_penny(idx[0],game_object.all_coordinates,game_object.penny_positions)
                                  game_object.killed_crows=game_object.killed_crows+1
                                  list_of_possible_kills = []
                                  game_object.current_player = 'crow' if game_object.current_player == 'vulture' else 'vulture'
                          else:
                            game_object.penny_positions[dragging_index][0]=inix
                            game_object.penny_positions[dragging_index][1]=iniy
                            game_object.display_alert("Kindly put the penny inside the circle !",1)
                         if(game_object.killed_crows >= 4):
                            game_object.running = False
                            game_object.result = 1
                            # display_alert_win("Hurray!  Vulture Won",4)
            else:
               game_object.wrong_turn = 0
               game_object.penny_positions[dragging_index][0]=game_object.x_befordrag
               game_object.penny_positions[dragging_index][1]=game_object.y_beforedrag
          else:
             game_object.click_on_space = 0
            
        elif event.type == pygame.MOUSEMOTION and dragging:
            # Update the position of the dragged penny
            mouse_x, mouse_y = event.pos
            game_object.penny_positions[dragging_index] = [mouse_x + offset_x, mouse_y + offset_y]

    screen.blit(image, image_rect)
    for pos in game_object.penny_positions[:-1]:
        pygame.draw.circle(screen, yellow, pos, game_object.penny_radius)
    pygame.draw.circle(screen, green, game_object.penny_positions[-1], game_object.penny_radius)
    crows_left = len(game_object.initial_positions) - game_object.killed_crows -1
    crows_left_text = font.render(f"Crows fighting: {crows_left}", True, (0,0,0))
    screen.blit(crows_left_text, (640, 10))
    crow_khtm = font.render(f"Crows killed: {game_object.killed_crows}", True, (0,0,0))
    screen.blit(crow_khtm, (650, 40))
    player_turn_text = font.render(f"Current turn: {game_object.current_player.capitalize()}", True, (0,0,0))
    screen.blit(player_turn_text, (20, 10))
    crow_text = font.render("Crow's Side", True, (0,0,0))
    vulture_text = font.render("Vulture's Side", True, (0,0,0))
    screen.blit(crow_text, (700,489))
    screen.blit(vulture_text, (36,518))
    if( game_object.result == 1):
      game_object.display_alert_win("Hurray!  Vulture Won",3)
      print("Hurray! Vulture Won")
    elif ( game_object.result == 0):
      game_object.display_alert_win("Hurray! Crows Won",3)
      print("Hurray! Crows Won")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

