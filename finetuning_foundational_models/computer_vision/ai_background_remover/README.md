# AI Background Remover

- Removing the background from a given image. 
- In this case, an object of interest is defined as the foreground object via mask
- Given the image along with the mask, the background will be removed

## 🛠️ Techniqual Details

- MVANet model was fine-tuned on a custom training dataset: [more details](https://github.com/VimukthiRandika1997/Background-Remover.git)
- Real images (1,000) + Synthetic images (3,000) were used to train the model
- Real product images were annotated using custom built annotation tool.

## 💡Current Progress

- Currently I am adapting a more powerful model like **BirefNet** for this task with a larget dataset (> 5,000 images) 