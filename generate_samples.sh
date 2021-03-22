#!/bin/bash

DIM=20
BOMBS_FOR_EVERY_10_PERCENT=$(expr $DIM \* $DIM / 10)
SAMPLES_PER_BOMB_COUNT=10

# Make our sample_data output dir
OUTPUT_DIR="./sample_data"
mkdir -p $OUTPUT_DIR

# output file paths
BASIC_OUTPUT="$OUTPUT_DIR/basic.txt"
ADVANCED_OUTPUT="$OUTPUT_DIR/advanced.txt"
HYPER_ADVANCED_OUTPUT="$OUTPUT_DIR/hyper_advanced.txt"
BONUS1_OUTPUT="$OUTPUT_DIR/bonus_1.txt"
BONUS2_OUTPUT="$OUTPUT_DIR/bonus_2.txt"


# Remove files if they already exist
if [ -f "$BASIC_OUTPUT" ]; then
  echo "$BASIC_OUTPUT already exists, so removing it."
  rm "$BASIC_OUTPUT"
fi
if [ -f "$ADVANCED_OUTPUT" ]; then
  echo "$ADVANCED_OUTPUT already exists, so removing it."
  rm "$ADVANCED_OUTPUT"
fi
if [ -f "$HYPER_ADVANCED_OUTPUT" ]; then
  echo "$HYPER_ADVANCED_OUTPUT already exists, so removing it."
  rm "$HYPER_ADVANCED_OUTPUT"
fi
if [ -f "$BONUS1_OUTPUT" ]; then
  echo "$BONUS1_OUTPUT already exists, so removing it."
  rm "$BONUS1_OUTPUT"
fi
if [ -f "$BONUS2_OUTPUT" ]; then
  echo "$BONUS2_OUTPUT already exists, so removing it."
  rm "$BONUS2_OUTPUT"
fi
echo -ne "Basic Agent Progress: (0%)\r"
#BASIC AGENT
for density in {0..10}
do
  bomb_count=$(expr $density \* $BOMBS_FOR_EVERY_10_PERCENT)
  echo "BOMB_COUNT = $bomb_count" >> $BASIC_OUTPUT
  for sample_num in $( eval echo {1..$SAMPLES_PER_BOMB_COUNT} )
  do
    curr_cmd="python3 main.py --dim $DIM --bomb_count $bomb_count --agent basic --quit_when_finished True"
    #"agent = " only appears in the line that contains the summary (the only part we are interested in)
    echo -e "\t$(eval $curr_cmd | grep -i "agent = ")" >> $BASIC_OUTPUT
  done
  echo -ne "Basic Agent Progress: ($(expr $(expr 1 + $density) \* 10)%)\r"
done

echo -e "\n"
echo -ne "Advanced Agent Progress: (0%)\r"
#ADVANCED AGENT
for density in {0..10}
do
  bomb_count=$(expr $density \* $BOMBS_FOR_EVERY_10_PERCENT)
  echo "BOMB_COUNT = $bomb_count" >> $ADVANCED_OUTPUT
  for sample_num in $( eval echo {1..$SAMPLES_PER_BOMB_COUNT} )
  do
    curr_cmd="python3 main.py --dim $DIM --bomb_count $bomb_count --agent advanced --quit_when_finished True"
    #"agent = " only appears in the line that contains the summary (the only part we are interested in)
    echo -e "\t$(eval $curr_cmd | grep -i "agent = ")" >> $ADVANCED_OUTPUT
  done
  echo -ne "Advanced Agent Progress: ($(expr $(expr 1 + $density) \* 10)%)\r"
done

echo "$HYPER_ADVANCED_OUTPUT"
echo -e "\n"
echo -ne "Hyper Advanced Agent Progress: (0%)\r"
# HYPER ADVANCED AGENT
for density in {0..10}
do
  bomb_count=$(expr $density \* $BOMBS_FOR_EVERY_10_PERCENT)
  echo "BOMB_COUNT = $bomb_count" >> $HYPER_ADVANCED_OUTPUT
  for sample_num in $( eval echo {1..$SAMPLES_PER_BOMB_COUNT} )
  do
    curr_cmd="python3 main.py --dim $DIM --bomb_count $bomb_count --agent hyper_advanced --quit_when_finished True"
    #"agent = " only appears in the line that contains the summary (the only part we are interested in)
    echo -e "\t$(eval $curr_cmd | grep -i "agent = ")" >> $HYPER_ADVANCED_OUTPUT
  done
  echo -ne "Hyper Advanced Agent Progress: ($(expr $(expr 1 + $density) \* 10)%)\r"
done

echo "$BONUS1_OUTPUT"
echo -e "\n"
echo -ne "Bonus 1 Agent Progress: (0%)\r"
# Bonus 1 ADVANCED AGENT
for density in {0..10}
do
  bomb_count=$(expr $density \* $BOMBS_FOR_EVERY_10_PERCENT)
  echo "BOMB_COUNT = $bomb_count" >> $BONUS1_OUTPUT
  for sample_num in $( eval echo {1..$SAMPLES_PER_BOMB_COUNT} )
  do
    curr_cmd="python3 main.py --dim $DIM --bomb_count $bomb_count --agent bonus_1 --quit_when_finished True"
    #"agent = " only appears in the line that contains the summary (the only part we are interested in)
    echo -e "\t$(eval $curr_cmd | grep -i "agent = ")" >> $BONUS1_OUTPUT
  done
  echo -ne "Bonus 1 Agent Progress: ($(expr $(expr 1 + $density) \* 10)%)\r"
done

echo "$BONUS2_OUTPUT"
echo -e "\n"
echo -ne "Bonus 2 Agent Progress: (0%)\r"
# Bonus 2 ADVANCED AGENT
for density in {0..10}
do
  bomb_count=$(expr $density \* $BOMBS_FOR_EVERY_10_PERCENT)
  echo "BOMB_COUNT = $bomb_count" >> $BONUS2_OUTPUT
  for sample_num in $( eval echo {1..$SAMPLES_PER_BOMB_COUNT} )
  do
    curr_cmd="python3 main.py --dim $DIM --bomb_count $bomb_count --agent bonus_2 --quit_when_finished True"
    #"agent = " only appears in the line that contains the summary (the only part we are interested in)
    echo -e "\t$(eval $curr_cmd | grep -i "agent = ")" >> $BONUS2_OUTPUT
  done
  echo -ne "Bonus 1 Agent Progress: ($(expr $(expr 1 + $density) \* 10)%)\r"
done



