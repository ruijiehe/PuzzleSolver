import numpy as np
import cv2
import time

import Functions_1 as F1
import Functions_2 as F2

Recalc_PT_bool = True

Recalc_PT_num = 10
Recalc_PT_count = 0

PT_bool = False         # Perform Perspective Transform
DP_bool = False         # Detect Pieces
CP_bool = False         # Clasify Pieces
SO_bool = False         # Seperate Overlapping Pieces
CP_bool = False         # Classify Piece

BoardSize=[757,508] #unit in mm
PieceMat=[6,4] 
PuzzlePCNT=24
edgenum=2*sum(PieceMat)
PuzzleSize=[284,220] #unit in mm
avgArea=int(np.ceil(PuzzleSize[0]*PuzzleSize[1]/float(PuzzlePCNT)))
##### Upper and lower boundries background [Calibration Values]
background_lower = np.array([0, 0, 140], dtype = "uint8") # [0, 0, 190] is somewhat gray in HSV
background_upper = np.array([255, 80, 255], dtype = "uint8") # [0, 0, 255] is white in HSV

avgPC_W=int(np.ceil(PuzzleSize[0]/float(PieceMat[0])))
avgPC_H=int(np.ceil(PuzzleSize[1]/float(PieceMat[1])))

print 'avgArea '+str(avgArea)+' PCwidth '+str(avgPC_W)+' PCheight '+str(avgPC_H)

filename='img.jpg'

pts_min = [[0, 0], [np.inf, 0], [np.inf, np.inf], [0, np.inf]]

while(True):
    img_ori = cv2.imread(filename)
    img = np.copy(img_ori)
   
    if PT_bool:
        img_C =F1.Perspective_Correction(img_ori,BoardSize)
        img = np.copy(img_C)
        if DP_bool: # detect piece
            #print 'detecting piece'
            img_B = F1.Clear_Background(img_C,background_lower,background_upper)
            img_BIN = F1.Binarise(img_B)
			F1.showimg(img_BIN)
            img_DP, piece_cnt, overlap_cnt = F1.Detect_Pieces(img_BIN, img_C, avgArea,PuzzlePCNT)
            img = np.copy(img_DP)
            if SO_bool and np.shape(overlap_cnt)[0] != 0:
                print 'solving overlap' +str(np.shape(overlap_cnt)[0])
                img_SO, From, To, Dir = F1.Separate_Overlap(img_BIN, img_DP, overlap_cnt)
                img = np.copy(img_SO)
            elif CP_bool and np.shape(overlap_cnt)[0] == 0 and np.shape(piece_cnt)[0] == PuzzlePCNT:
                print "Classifying pieces"                
                CP_time = time.clock()
                classify_successful, Piece = F1.Classify_Pieces(img_B, piece_cnt, edgenum, avgPC_W, avgPC_H)
                CP_time = time.clock() - CP_time
                if classify_successful:
                    CP_bool = False
                    img_CLA = F2.Draw_Classification(Piece)
                    cv2.imshow("Classification", img_CLA)
                    print "\nClassification Time = ", CP_time*1000, " ms\n"
                    if SOLVE_bool:
                        print "solving puzzle"
                        SOLVE_time = time.clock()
                        solution_successful, Solution_Piece, img_Solution = F2.Solve_Puzzle(Piece)
                        SOLVE_time = time.clock() - SOLVE_time
                        if solution_successful:
                            SOLVE_bool = False
                            cv2.imshow("Puzzle Solution", img_Solution)
                            print "\nSolution Time = ", SOLVE_time*1000, " ms\n"
                        else:
                            CP_bool = True
        else:
            img = F1.Perspective_Correction(img_ori,BoardSize)

    # Display the resulting img_ori
    cv2.imshow("Puzzle",img)

    k = cv2.waitKey(1)
    if k == ord("q"):       # Quit
        break
    #elif k == ord("1"):     # Recalclculate Points
        #pts_min = [[0, 0], [np.inf, 0], [np.inf, np.inf], [0, np.inf]]
        #Recalc_PT_bool = True
        #Recalc_PT_count = 0
    elif k == ord("2"):     # Perform Perspective Transform
        PT_bool = not PT_bool
        print 'PT_bool'+' '+str(PT_bool)
        DP_bool = False
        SO_bool = False
        CP_bool = False
        SOLVE_bool = False
    elif k == ord("3"):     # Detect Pieces
        PT_bool = True
        DP_bool = not DP_bool
        print 'DP_bool'+' '+str(DP_bool)
        SO_bool = False
        CP_bool = False
        SOLVE_bool = False
    elif k == ord("4"):     # Seperate Overlapping Pieces
        PT_bool = True
        DP_bool = True
        SO_bool = not SO_bool
        print 'SO_bool'+' '+str(SO_bool)
        CP_bool = False
        SOLVE_bool = False
    elif k == ord("5"):     # Classify Pieces
        PT_bool = True
        DP_bool = True
        SO_bool = True
        CP_bool = not CP_bool
        print 'CP_bool'+' '+str(CP_bool)
        SOLVE_bool = False
    elif k == ord("6"):     # Solve Puzzle
        PT_bool = True
        DP_bool = True
        SO_bool = True
        CP_bool = True
        SOLVE_bool = not SOLVE_bool
        print 'SOLVE_bool'+' '+str(SOLVE_bool)
    elif k == ord("k"):     # Capture Images
        folder = "images"
        cv2.imwrite(folder+"/OG.png",img_ori)
        if DP_bool:
            cv2.imwrite(folder+"/PT.png",img_C)
            cv2.imwrite(folder+"/B.png",img_B)
            cv2.imwrite(folder+"/BIN.png",img_BIN)
            cv2.imwrite(folder+"/DP.png",img_DP)
            if img_SO != []:
                cv2.imwrite(folder+"/SO.png",img_SO)
            if img_CLA != []:
                cv2.imwrite(folder+"/CLA.png",img_CLA)
            if img_Solution != []:
                cv2.imwrite(folder+"/SOL.png",img_Solution)

# When everything done, release the capture
cv2.destroyAllWindows()
