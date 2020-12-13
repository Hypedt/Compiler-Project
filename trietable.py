import os

class TrieTable:
    maxTransitions = 25
    # stores index if switch uppercase: 0-25, lowercase: 26-51
    switchArray = [-1] * 52
    # stores symbols in id's
    symbolArray = ['*'] * maxTransitions
    # stores index of next id
    nextArray = [-1] * maxTransitions
    # tracks end of symbol array
    symbolPointer = 0

    # Print the trie table.
    def printTrie(self):
        capLetters = "   A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z"
        lowLetters = "  a   b   c   d   e   f   g   h   i   j   k   l   m   n   o   p   q   r   s   t   u   v   w   x   y   z"
        letterIndex = ""
        index = ""
        switch = ""
        symbol = ""
        nextSet = ""

        #This will format the strings
        for i in range(len(self.switchArray)):
            switch += "{:4d}".format(self.switchArray[i])
        for i in range(len(self.symbolArray)):
            index += "{:4d}".format(i)
            symbol += "{:4c}".format(ord(self.symbolArray[i]))
            nextSet += "{:4d}".format(self.nextArray[i])

        # print the formatted strings
        print("")
        print("        ", capLetters, lowLetters)
        print("switchArray: ", switch)
        print()
        print("        ", index)
        print("symbolArray: ", symbol)
        print("nextSet:   ", nextSet)

    # Write the formatted trie table to a specified file
    def printTrieToFile(self, file):
        capLetters = "   A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z"
        lowLetters = "   a   b   c   d   e   f   g   h   i   j   k   l   m   n   o   p   q   r   s   t   u   v   w   x   y   z"
        letterIndex = ""
        index = ""
        switch = ""
        symbol = ""
        nextSet = ""

        #This will format the strings
        for i in range(len(self.switchArray)):
            switch += "{:4d}".format(self.switchArray[i])
        for i in range(len(self.symbolArray)):
            index += "{:4d}".format(i)
            symbol += "{:4c}".format(ord(self.symbolArray[i]))
            nextSet += "{:4d}".format(self.nextArray[i])

        # split strings
        charCountPerRow = 90
        allLetters = capLetters + lowLetters
        splitLetters = [allLetters[y-charCountPerRow:y] for y in range(charCountPerRow, len(allLetters)+charCountPerRow, charCountPerRow)]
        splitSwitch = [switch[y-charCountPerRow:y] for y in range(charCountPerRow, len(switch)+charCountPerRow,charCountPerRow)]
        splitIndex = [index[y-charCountPerRow:y] for y in range(charCountPerRow, len(index)+charCountPerRow,charCountPerRow)]
        splitSymbol = [symbol[y-charCountPerRow:y] for y in range(charCountPerRow, len(symbol)+charCountPerRow,charCountPerRow)]
        splitNext = [nextSet[y-charCountPerRow:y] for y in range(charCountPerRow, len(nextSet)+charCountPerRow,charCountPerRow)]


        # check that file can be written to
        if not os.access(file.name, os.W_OK):
            print("Cannot write to file.")
            return

        # print the formatted strings
        file.write("\n")
        for stringIndex in range(len(splitLetters)):
            file.write("        " + splitLetters[stringIndex] + "\n")
            file.write("switch: " + splitSwitch[stringIndex] + "\n")
            file.write("\n")
        file.write("\n\n")
        for stringIndex in range(len(splitIndex)):
            file.write("        " + splitIndex[stringIndex] + "\n")
            file.write("symbol: " + splitSymbol[stringIndex] + "\n")
            file.write("next:   " + splitNext[stringIndex] + "\n")
            file.write("\n")

    # Grow the trie table.
    def growTable(self):
        temp1 = ['*'] * self.maxTransitions
        temp2 = [-1] * self.maxTransitions
        self.symbolArray = self.symbolArray + temp1
        self.nextArray = self.nextArray + temp2
        self.maxTransitions = self.maxTransitions * 2

    # Returns the index of the corresponding letter in the switchArray
    # Reutnr -1 if it is not in the array
    def switchIndexOfSymbol(self, c):
        asciiValue = ord(c)
        if (asciiValue > 64 and asciiValue < 91):
            return asciiValue - 65
        elif (asciiValue > 96 and asciiValue < 123):
            return asciiValue - 71
        else:
            return -1

    # Creates identifiers.
    def createID(self, identifier, ptr):

        # if no id contains this first letter
        if (ptr == -1):

            # store index of first undefined symbol in symbol array to switchArray
            ptr = self.symbolPointer
            self.switchArray[self.switchIndexOfSymbol(identifier[0])] = ptr

            # fill in symbolArray array
            x = 1
            i = self.symbolPointer
            while ((ptr - i) != len(identifier) - 1):
                self.symbolArray[ptr] = identifier[x]
                x += 1
                ptr += 1
                self.symbolPointer += 1

                # if its the end of the table, double the size
                if (self.symbolPointer == self.maxTransitions): self.growTable()

            # add terminal symbolArray
            self.symbolArray[ptr] = '@'
            self.symbolPointer += 1

            # if its the end of the table, double the size
            if (self.symbolPointer == self.maxTransitions): self.growTable()

        else:

            # store index of first undefined symbol in symbolArray to nextArray
            self.nextArray[ptr] = self.symbolPointer

            # fill the symbol array
            ptr = self.symbolPointer
            i = self.symbolPointer
            x = 0

            # while not at the last symbolArray
            while ((ptr - i) != len(identifier)):
                self.symbolArray[ptr] = identifier[x]
                x += 1
                ptr += 1
                self.symbolPointer += 1

                # double size at the end of the table
                if (self.symbolPointer == self.maxTransitions): self.growTable()

            self.symbolArray[ptr] = '@'
            self.symbolPointer += 1

            if (self.symbolPointer == self.maxTransitions): self.growTable()

        return

    # Search whether an identifier exists.
    def searchAndCreateIDs(self, identifier):
        # if empty return false
        if (not identifier): return False

       #swtich index of symbol array
        index = 0
        valueOfSymbol = self.switchIndexOfSymbol(identifier[index])

        # if identifier does not start with a letter
        if (valueOfSymbol == -1): return False

        # create a new identifier if there are no indentifers with that letter
        ptr = self.switchArray[valueOfSymbol]
        if (ptr == -1):
            self.createID(identifier, ptr)

        #identifier that starts with id[0]
        else:

            exitLoop = False

            # get ascii of nextSet char
            if (len(identifier) > 1):
                index += 1
                valueOfSymbol = ord(identifier[index])
            # if unique
            elif (self.nextArray[self.switchArray[self.switchIndexOfSymbol(identifier)]] == -1):
                self.nextArray[self.switchArray[self.switchIndexOfSymbol(identifier)]] = self.symbolPointer
                self.symbolArray[self.symbolPointer] = '@'
                self.symbolPointer += 1

                # if its the end of the table, double the size
                if (self.symbolPointer == self.maxTransitions): self.growTable()
                return True
            else:
                return False

            # compare the chars in id with chars in symbol
            while (not exitLoop):

                # if its not a valid, return false
                valueOfID = ord(identifier[index])
                if (valueOfID != 95 and
                        (valueOfID < 65 or valueOfID > 90) and
                        (valueOfID < 97 or valueOfID > 122) and
                        (valueOfID < 48 or valueOfID > 57)): return False

                # if symbol array contains current char
                if (ord(self.symbolArray[ptr]) == valueOfSymbol):
                    #check the next char in id if the current char is not found at the end
                    if (index != len(identifier) - 1):
                        ptr += 1
                        index += 1
                        valueOfSymbol = ord(identifier[index])

                    else:
                        exitLoop = True
                        nextIndexValue = ptr + 1
                        while (self.nextArray[nextIndexValue] != -1):
                            nextIndexValue = self.nextArray[nextIndexValue]

                        # if identifier is unique add it to table
                        if (self.symbolArray[nextIndexValue] != '@'):
                            # if its the end of the table, double the size
                            if (self.symbolPointer == self.maxTransitions): self.growTable()
                            self.nextArray[nextIndexValue] = self.symbolPointer
                            self.symbolArray[self.symbolPointer] = '@'
                            self.symbolPointer += 1

                        else:
                            return False

                elif (self.nextArray[ptr] != -1):
                    ptr = self.nextArray[ptr]

                #create new identifier
                else:
                    self.createID(identifier[index:], ptr)
                    exitLoop = True

        return True


