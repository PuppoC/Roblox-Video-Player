import cv2 as cv
import time
import json

def rescaleFrame(frame, scale = 0.75):

    width = int(frame.shape[1]* scale)
    height = int(frame.shape[0] * scale)

    return cv.resize(frame, (width,height), interpolation = cv.INTER_AREA)


def getPixelData(videoLocation,resolutionMulti,cFPS,colour):

    videoCapture = cv.VideoCapture(videoLocation)
    totalFrames = int(videoCapture.get(cv.CAP_PROP_FRAME_COUNT))

    printVideoProperties = True

    frameIterations = 0
    realFrameIterations = 0

    prevPercentageCompleted = 0

    prevTime = time.time()


    finalTable = []

    while True:

        success, frame = videoCapture.read()

        if not success:
            continue

        currentTime = time.time()
        deltaTime = currentTime - prevTime

        if deltaTime > 1/cFPS:

            prevTime = currentTime

            #cv.imshow('Video',frame)

            frame = rescaleFrame(frame,resolutionMulti)

            if printVideoProperties:
                print("Resolution:",frame.shape)
                printVideoProperties = False


            xTable = []

            for x in range(frame.shape[1]):

                yTable = []

                for y in range(frame.shape[0]):

                    if colour:

                       cTable = [int(frame[y,x,2]),int(frame[y,x,1]),int(frame[y,x,0])]

                    else:

                        greyScale = round((float(frame[y,x,2]) + float(frame[y,x,1]) + float(frame[y,x,0]))/3)

                        cTable = [int(greyScale)]

                    yTable.insert(len(yTable)-1, cTable)

                xTable.insert(len(xTable)-1, yTable)


            finalTable.insert(len(finalTable)-1, xTable)

            realFrameIterations += 1


        frameIterations += 1

        percentageCompleted = round((frameIterations/totalFrames)*100)

        if percentageCompleted > prevPercentageCompleted:

            print("Progress:",str(percentageCompleted) + "%")
            prevPercentageCompleted = percentageCompleted


        if cv.waitKey(1) & 0xFF == ord('d'):
            break

        if frameIterations >= totalFrames:
            break


    videoCapture.release()
    cv.destroyAllWindows()

    return finalTable

pixelData = getPixelData("Resources/Videos/BadApple.mp4",.1,30,False)
print("Pixel Data Processed")


print("Encoding into JSON Data")
jsonEncoded = json.dumps(pixelData,sort_keys = True)
print("Encoded")

print("Opening file")
dumpFile = open("Resources/PixelData/BadApple.txt",'w')

print("Writing file")
dumpFile.write(jsonEncoded)

print("Closing file")
dumpFile.close()

print("Encryption Completed")

